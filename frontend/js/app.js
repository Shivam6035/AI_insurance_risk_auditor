document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const queryInput = document.getElementById('policy-query');
    const auditBtn = document.getElementById('audit-btn');
    const resetBtn = document.getElementById('reset-btn');
    const errorMsg = document.getElementById('error-message');

    // Sections
    const inputSection = document.getElementById('input-section');
    const loadingSection = document.getElementById('loading-section');
    const resultsSection = document.getElementById('results-section');

    // Result Elements
    const resProvider = document.getElementById('res-provider');
    const resPolicyName = document.getElementById('res-policy-name');
    const resVerdict = document.getElementById('res-verdict');
    const resScore = document.getElementById('res-score');
    const scoreRing = document.getElementById('score-ring');
    const deductionsCount = document.getElementById('deductions-count');
    const deductionsTableBody = document.getElementById('deductions-table-body');

    // --- Quick Prompt Buttons ---
    document.querySelectorAll('.quick-prompt').forEach(button => {
        button.addEventListener('click', (e) => {
            queryInput.value = `Audit my ${e.target.innerText} policy.`;
        });
    });

    // --- Main Audit Action ---
    auditBtn.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        
        if (!query) {
            showError("Please enter a policy to audit.");
            return;
        }

        // 1. Transition to Loading State
        inputSection.classList.add('hidden');
        errorMsg.classList.add('hidden');
        loadingSection.classList.remove('hidden');

        try {
            // 2. Fetch data from FastAPI backend
            const response = await fetch('http://localhost:8000/api/v1/audit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_query: query })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "An error occurred while auditing the policy.");
            }

            const data = await response.json();
            
            // 3. Render the Results
            renderResults(data);

        } catch (err) {
            // 4. Handle Errors (Revert to input state)
            loadingSection.classList.add('hidden');
            inputSection.classList.remove('hidden');
            showError(err.message);
        }
    });

    // --- Render Logic ---
    function renderResults(data) {
        // Populate Top Cards
        resProvider.innerText = data.provider || "Unknown Provider";
        resPolicyName.innerText = data.policy_name || "Unknown Policy";
        resVerdict.innerText = data.verdict || "No verdict provided.";
        
        // Populate and Color Score
        const score = data.final_score || 0;
        resScore.innerText = score;
        
        // Reset base classes for the score ring
        scoreRing.className = "relative w-36 h-36 flex items-center justify-center rounded-full border-[10px] shadow-inner mb-3 transition-colors duration-500";
        
        // Apply color thresholds
        if (score >= 800) {
            scoreRing.classList.add('border-green-500'); // Excellent
        } else if (score >= 600) {
            scoreRing.classList.add('border-yellow-400'); // Warning
        } else {
            scoreRing.classList.add('border-red-500'); // Danger
        }

        // Populate Deductions Table
        deductionsTableBody.innerHTML = ""; // Clear old data
        const deductions = data.deductions || [];
        
        if (deductions.length === 0) {
            deductionsCount.innerText = "0 found";
            deductionsCount.className = "text-xs font-semibold text-green-700 bg-green-100 py-1 px-2 rounded";
            deductionsTableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="px-6 py-8 text-center text-gray-500 font-medium">
                        Perfect score! No hidden penalties found.
                    </td>
                </tr>
            `;
        } else {
            deductionsCount.innerText = `${deductions.length} found`;
            deductionsCount.className = "text-xs font-semibold text-red-700 bg-red-100 py-1 px-2 rounded";
            
            deductions.forEach(item => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-gray-50 transition-colors";


                // --- NEW: Populate Improvement Suggestions ---
        const suggestionsList = document.getElementById('suggestions-list');
        suggestionsList.innerHTML = ''; // Clear previous results

        if (data.improvement_suggestions && data.improvement_suggestions.length > 0) {
            data.improvement_suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.className = 'flex items-start gap-3 bg-white p-4 rounded-lg border border-emerald-50 shadow-sm';
                li.innerHTML = `
                    <div class="mt-1 flex-shrink-0">
                        <!-- Green checkmark icon -->
                        <svg class="w-5 h-5 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                    </div>
                    <div>
                        <p class="text-gray-800 font-semibold leading-snug">${suggestion.recommendation}</p>
                        <p class="text-xs text-gray-500 mt-1.5 font-medium">
                            <span class="uppercase tracking-wider text-emerald-600 font-bold mr-1">Source:</span> 
                            ${suggestion.source_citation}
                        </p>
                    </div>
                `;
                suggestionsList.appendChild(li);
            });
        } else {
            suggestionsList.innerHTML = `
                <li class="text-gray-500 italic p-4 text-center">
                    No specific improvements identified. Your policy coverage is well-optimized!
                </li>
            `;
        }
                
                // Handle missing URLs gracefully
                const sourceHtml = (item.source_url && item.source_url.startsWith('http'))
                    ? `<a href="${item.source_url}" target="_blank" class="text-blue-600 hover:text-blue-800 hover:underline text-sm font-medium">View Source &rarr;</a>`
                    : `<span class="text-gray-400 text-sm">Not available</span>`;

                tr.innerHTML = `
                    <td class="px-6 py-4 border-b border-gray-100 font-medium text-gray-900">${item.category}</td>
                    <td class="px-6 py-4 border-b border-gray-100 text-red-600 font-bold">${item.penalty}</td>
                    <td class="px-6 py-4 border-b border-gray-100 text-sm text-gray-600">${item.reason}</td>
                    <td class="px-6 py-4 border-b border-gray-100 text-right">${sourceHtml}</td>
                `;
                deductionsTableBody.appendChild(tr);
            });
        }

        // Transition to Results State
        loadingSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
    }

    // --- Reset Action ---
    resetBtn.addEventListener('click', () => {
        resultsSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
        queryInput.value = '';
    });

    // --- Error Helper ---
    function showError(message) {
        errorMsg.innerText = message;
        errorMsg.classList.remove('hidden');
    }
});