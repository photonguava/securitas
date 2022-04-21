from fastapi import FastAPI
from pydantic import BaseModel
from tortoise.fields.base import CASCADE

from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
app = FastAPI()


class Project(Model):
    id = fields.IntField(pk=True)
    app_name = fields.CharField(200)
    scope = fields.CharField(200)
    vulnerabilities : fields.ReverseRelation['Vulnerability']

class Vulnerability(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(3000)
    description = fields.CharField(90000)
    fixes = fields.CharField(90000)
    severity = fields.CharField(500)
    url = fields.CharField(10000)
    refs = fields.CharField(10000)

    project : fields.ForeignKeyRelation[Project] = fields.ForeignKeyField(
        "models.Project",
        related_name="vulnerabilities"
    )

# userPydantic = pydantic_model_creator(User,name='User')
# userInPydantic = pydantic_model_creator(User,name="UserIn",exclude_readonly=True)
projectPydantic = pydantic_model_creator(Project,name='Project')
projectInPydantic = pydantic_model_creator(Project,name="ProjectIn",exclude_readonly=True)
vulnerabilityPydantic = pydantic_model_creator(Vulnerability,name='Vulnerability')
vulnerabilityInPydantic = pydantic_model_creator(Vulnerability,name="VulnerabilityIn",exclude_readonly=True)

# @app.post('/user')
# async def create_user(user: userInPydantic):
#     user_obj = await User.create(**user.dict())
#     return await userPydantic.from_tortoise_orm(user_obj)

# @app.post('/user/{username}/project')
# async def create_project(username: str, project: projectInPydantic):
#     user_obj = await User.get(username=username)
#     project_obj = await Project.create(scope=project.scope,app_name=project.app_name,user=user_obj)
#     x = await projectPydantic.from_tortoise_orm(project_obj)
#     return x.id

# @app.get('/user')
# async def get_users():
#     return await userPydantic.from_queryset(User.all())

@app.get('/projects')
async def get_projects():
    return await projectPydantic.from_queryset(Project.all())

@app.get('/projects/{project_id}')
async def get_project(proj_id: int):
    proj_obj = await Project.get(id=proj_id)
    return await proj_obj

@app.post('/projects/{project_id}/vulnerabilities')
async def create_vulnerability(project_id: int,vulnerability: vulnerabilityInPydantic):
    project_obj = await Project.get(id=project_id)
    return await Vulnerability.create(title = vulnerability.title,description = vulnerability.description,fixes = vulnerability.fixes, severity=vulnerability.severity,project=project_obj,refs=vulnerability.refs,url=vulnerability.url)
    
@app.post('/projects')
async def create_project(project: projectInPydantic):
    proj_obj = await Project.create(app_name=project.app_name,scope=project.scope)
    return proj_obj.id


@app.get('/projects/{project_id}/vulnerabilities')
async def get_vulnerabilities(project_id: int):
    project_obj = await Project.get(id=project_id)
    return await project_obj.vulnerabilities

@app.get('/vulnerabilities/{vuln_id}')
async def get_vulnerabilities(vuln_id: int):
    vuln_obj = await Vulnerability.get(id=vuln_id)
    return await vuln_obj

register_tortoise(
    app,
    db_url = "sqlite://db.sqlite3",
    modules = {'models': ['main']},
    generate_schemas=True,
)
