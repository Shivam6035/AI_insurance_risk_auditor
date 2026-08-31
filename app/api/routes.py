# import json
# from fastapi import APIRouter, HTTPException, status
# from langchain_core.messages import HumanMessage

# from app.models.request import AuditRequest
# from app.models.response import AuditResponse
# from app.agent.graph import auditor_agent

# # Note: Do not put a prefix here.
# router = APIRouter(tags=["Auditor"])

# @router.post(
#     "/audit",
#     response_model=AuditResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Audit an insurance policy"
# )
# async def audit_policy(request: AuditRequest):
#     try:
#         final_state = await auditor_agent.ainvoke(
#             {"messages": [HumanMessage(content=request.user_query)]}
#         )

#         last_message = final_state["messages"][-1]
#         raw_content = last_message.content

#         if "```json" in raw_content:
#             raw_content = raw_content.split("```json")[1].split("```")[0].strip()
#         elif "```" in raw_content:
#             raw_content = raw_content.split("```")[1].split("```")[0].strip()

#         data = json.loads(raw_content)
#         return AuditResponse(**data)

#     except json.JSONDecodeError as err:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Agent failed to return valid structured JSON: {str(err)}"
#         )
#     except Exception as err:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Audit execution error: {str(err)}"
#         )

import json
from fastapi import APIRouter, HTTPException, status
from langchain_core.messages import HumanMessage

from app.models.request import AuditRequest
from app.models.response import AuditResponse
from app.agent.graph import auditor_agent

router = APIRouter(tags=["Auditor"])

@router.post(
    "/audit",
    response_model=AuditResponse,
    status_code=status.HTTP_200_OK,
    summary="Audit an insurance policy"
)
async def audit_policy(request: AuditRequest):
    try:
        final_state = await auditor_agent.ainvoke(
            {"messages": [HumanMessage(content=request.user_query)]}
        )

        last_message = final_state["messages"][-1]
        raw_content = last_message.content

        # FIX: Handle Gemini's list-based content blocks
        if isinstance(raw_content, list):
            # Extract text from the dictionary blocks
            extracted_text = ""
            for block in raw_content:
                if isinstance(block, dict) and "text" in block:
                    extracted_text += block["text"]
                elif isinstance(block, str):
                    extracted_text += block
            raw_content = extracted_text

        # Ensure raw_content is a string before regex/splitting
        raw_content = str(raw_content).strip()

        # Strip markdown code blocks if the LLM wrapped the JSON
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1].split("```")[0].strip()

        data = json.loads(raw_content)
        return AuditResponse(**data)

    except json.JSONDecodeError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent failed to return valid structured JSON: {str(err)}"
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audit execution error: {str(err)}"
        )