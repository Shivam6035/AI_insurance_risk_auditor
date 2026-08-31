document.addEventListener('DOMContentLoaded', () => {
    const btnCompare = document.getElementById('compare-btn');
    const btnExport = document.getElementById('export-pdf-btn');
    const inputA = document.getElementById('policy-a');
    const inputB = document.getElementById('policy-b');
    const errObj = document.getElementById('error-message');
    
    const sections = {
        input: document.getElementById('input-section'),
        loading: document.getElementById('loading-section'),
        results: document.getElementById('results-section')
    };

    btnCompare.addEventListener('click', async () => {
        if (!inputA.value || !inputB.value) {
            errObj.innerText = "Please enter both policies.";
            errObj.classList.remove('hidden');
            return;
        }

        errObj.classList.add('hidden');
        sections.loading.classList.remove('hidden');
        sections.results.classList.add('hidden');

        try {
            const response = await fetch('/api/v1/compare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ policy_a: inputA.value.trim(), policy_b: inputB.value.trim() })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Server error occurred");
            }
            
            populateDashboard(data);
            
            sections.loading.classList.add('hidden');
            sections.results.classList.remove('hidden');

        } catch (err) {
            console.error("Comparison Error:", err);
            sections.loading.classList.add('hidden');
            errObj.innerText = `Error: ${err.message}`;
            errObj.classList.remove('hidden');
        }
    });

    function populateDashboard(data) {
        document.getElementById('res-name-a').innerText = data.policy_a_name;
        document.getElementById('res-name-b').innerText = data.policy_b_name;
        document.getElementById('res-winner').innerText = data.winner;
        document.getElementById('res-summary').innerText = data.executive_summary;

        // Render Chart
        renderRadarChart(data.chart_data, data.policy_a_name, data.policy_b_name);

        // Populate Grid
        const grid = document.getElementById('detailed-analysis-grid');
        grid.innerHTML = ""; 
        
        for (const [metric, analysis] of Object.entries(data.detailed_analysis)) {
            grid.innerHTML += `
                <div class="bg-white p-5 border border-gray-100 rounded-lg shadow-sm">
                    <h4 class="font-bold text-gray-900 uppercase tracking-wide text-xs mb-2">${metric}</h4>
                    <p class="text-sm text-gray-600">${analysis}</p>
                </div>
            `;
        }
    }

    // PDF Export Implementation
    btnExport.addEventListener('click', () => {
        const element = document.getElementById('results-section');
        
        // Temporarily hide UI elements not meant for the PDF
        const noPrintElements = element.querySelectorAll('.no-print');
        noPrintElements.forEach(el => el.style.display = 'none');

        const opt = {
            margin: 0.5,
            filename: 'comparative_policy_report.pdf',
            image: { type: 'jpeg', quality: 1 },
            html2canvas: { scale: 2, useCORS: true },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };

        html2pdf().set(opt).from(element).save().then(() => {
            // Restore UI elements after PDF generates
            noPrintElements.forEach(el => el.style.display = '');
        });
    });
});