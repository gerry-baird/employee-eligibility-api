from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.routing import APIRoute
from fastapi.security import HTTPBasic, HTTPBasicCredentials

description = """
Employee Eligibility API helps you do awesome stuff. 🚀

## Candidates

This API allows you to view, add and update candidates. You will be able to:

* **View a candidate**
* **View ALL candidate**
* **View the next candidate ready for onboarding**
* **Set the status of a candidate to onboarding**
* **Add a candidate**

* **Filter candidates using Neural Network** (_not implemented_).
"""


app = FastAPI(
    title="Employee Eligibility",
    description=description,
    summary="Employee Eligibility",
    version="1.8",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Gerry Baird",
        "url": "https://github.com/gerry-baird/employee-eligibility-api",
        "email": "gerry.baird@uk.ibm.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

security = HTTPBasic()


class Message(BaseModel):
    message: str


class Candidate(BaseModel):
    id: int
    name: str
    status: str
    dob: date
    position: str
    location: str
    dept: str
    eligibility: str
    ref: str


class CandidateIdentifier(BaseModel):
    id: int
    ref: str


class CandidateList(BaseModel):
    candidates: list[Candidate]

def regenCandidates():
    return [
        Candidate(id=1, name="Waheed Haris Rinaldi", status="Accepted", dob="1990-03-11",
                  position="Marketing Analyst", location="London", dept="A01", eligibility="Pending", ref=""),
        Candidate(id=2, name="Venkat Bonaventura Telman", status="Accepted", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref=""),
        Candidate(id=3, name="Oriana Telama Byrd", status="Accepted", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref=""),
        Candidate(id=4, name="Kamilla Vitia Campo", status="Accepted", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref=""),
        Candidate(id=5, name="Waheed Haris Rinaldi", status="Accepted", dob="1990-03-11",
                  position="Marketing Analyst", location="London", dept="A01", eligibility="Pending", ref=""),
        Candidate(id=6, name="Venkat Bonaventura Telman", status="Accepted", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref=""),
        Candidate(id=7, name="Oriana Telama Byrd", status="Accepted", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref=""),
        Candidate(id=8, name="Kamilla Vitia Campo", status="Accepted", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref=""),
        Candidate(id=101, name="Freddy Mercury", status="Interview", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref=""),
        Candidate(id=102, name="David Bowie", status="Rejected", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref=""),
        Candidate(id=103, name="Tina Turner", status="Assessment", dob="1991-04-11",
                  position="IT Developer", location="LA", dept="B01", eligibility="Pending", ref="")
    ]


# this is our datastore
pre_baked_candidates = regenCandidates()


@app.get("/",
         summary='Employee Eligibility Ping',
         description='Employee Eligibility Ping',
         response_description="Employee Eligibility Ping"
         )
async def greeting(credentials: HTTPBasicCredentials = Depends(security)) -> Message:
    return {"message": "Employee Eligibility is Alive"}


@app.get("/candidate/{id}",
         summary='View a candidate',
         description='View a candidate',
         response_description="The candidate details")
def get_candidate(id: int) -> Candidate:
    for candidate in pre_baked_candidates:
        if candidate.id == id:
            return candidate

    raise HTTPException(status_code=404, detail="Candidate not found")


@app.get("/candidates",
         summary='View all candidates',
         description='View all candidates',
         response_description="All the candidate details")
def getCandidates() -> CandidateList:

    all_candidates = CandidateList(candidates = pre_baked_candidates)

    return all_candidates


@app.get("/onboarding",
         summary='Next candidate ready for onboarding',
         description='Next candidate ready for onboarding',
         response_description="The candidate details")
def getNextCandidateForOnboarding() -> Candidate:
    for candidate in pre_baked_candidates:
        if candidate.status == "Accepted":
            return candidate


@app.post(
    '/setStatusOnboarding',
    summary='Set candidate status to onboarding',
    description='Set candidate status to onboarding',
    response_description="Updated candidate"
)
def updateToOnboarding(identifier: CandidateIdentifier) -> Candidate:
    target_id = identifier.id

    for candidate in pre_baked_candidates:
        if candidate.id == target_id:
            target_candidate: Candidate = candidate

    if target_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    else:
        target_candidate.status = "Onboarding"
        target_candidate.ref = identifier.ref

    return target_candidate


@app.post('/reset',
          summary='Reset',
          description='Resets all candidates to initial state',
          response_description="All candidate details")
def reset() -> CandidateList:
    global pre_baked_candidates
    pre_baked_candidates = regenCandidates()

    all_candidates = CandidateList(candidates=pre_baked_candidates)

    return all_candidates


@app.post('/candidate',
    summary = 'Add Candidate',
    description = 'Add Candidate',
    response_description = "New Candidate")
def addCandidate(newCandidate: Candidate) -> Candidate:

    # find the maximum ID in the existing candidates
    max_id = 0
    for candidate in pre_baked_candidates:
        if candidate.id > max_id:
            max_id = candidate.id

    newCandidate.id = max_id + 1
    pre_baked_candidates.append(newCandidate)
    return newCandidate


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, operation ID will be 'greeting'


use_route_names_as_operation_ids(app)
