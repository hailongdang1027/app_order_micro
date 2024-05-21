from uuid import UUID

import httpx
from fastapi import FastAPI, APIRouter, Request, Depends
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from microservice_food_app.app_food.app.models.food import CreateFoodModel
from microservice_food_app.app_order.app.models.order import CreateOrder
from microservice_food_app.gate_api.app.endpoints.auth_router import get_user_role, auth_router

host_ip = "192.168.222.131"
auth_url = "http://localhost:8000/auth/login"

# logging.basicConfig()

app = FastAPI(title='Service')

user_router = APIRouter(prefix='/user', tags=['user'])
staff_router = APIRouter(prefix='/staff', tags=['staff'])
app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')

MICROSERVICES = {
    "food": "http://localhost:83/api",
    "order": "http://localhost:84/api",
}


def proxy_request(service_name: str, path: str, user_info, request: Request, json_data: dict = None):
    url = f"{MICROSERVICES[service_name]}{path}"
    timeout = 20
    headers = {
        'user': str(user_info)
    }
    print(request.method)
    if request.method == 'GET':
        response = httpx.get(url, headers=headers, timeout=timeout).json()
    elif request.method == 'POST':
        response = httpx.post(url, headers=headers, json=json_data, timeout=timeout).json()
    elif request.method == 'PUT':
        response = httpx.put(url, headers=headers, json=json_data).json()
    elif request.method == 'DELETE':
        response = httpx.delete(url, headers=headers).json()

    return response


# ___food___

@staff_router.get("/food")
def read_food(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        print(f"\nrequest.session['prev_url'] = {request.session['prev_url']}\n")
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path="/food/", user_info=current_user, request=request)


@user_router.post("/food/add", response_model=CreateFoodModel)
def add_food(request: Request, food_request: CreateFoodModel, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path="/food/add", user_info=current_user, request=request,
                             json_data=food_request.dict())


@staff_router.post("/food/add", response_model=CreateFoodModel)
def add_food(request: Request, food_request: CreateFoodModel, current_user: dict = Depends(get_user_role)):
    print(f"\n/food/add\n")
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path="/food/add", user_info=current_user, request=request,
                             json_data=food_request.dict())


@user_router.get("/food/{id}")
def read_food_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path=f"/food/{id}", user_info=current_user, request=request)


@staff_router.get("/food/{id}")
def read_food_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path=f"/food/{id}", user_info=current_user, request=request)


@staff_router.post('/food/{id}/delete')
def delete_food(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path=f"/food/{id}/delete", user_info=current_user, request=request)


@staff_router.post("/order/add", response_model=CreateOrder)
def add_order(request: Request, order_request: CreateOrder, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        print(f'add_order == {order_request}')
        return proxy_request(service_name="order", path="/order/add", user_info=current_user, request=request,
                             json_data=order_request.dict())


@user_router.post("/order/add", response_model=CreateOrder)
def add_order(request: Request, order_request: CreateOrder, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        print(f'add_order == {order_request}')
        return proxy_request(service_name="receipt", path="/order/add", user_info=current_user, request=request,
                             json_data=order_request.dict())


@staff_router.get("/order")
def read_order(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        print(f"\nrequest.session['prev_url'] = {request.session['prev_url']}\n")
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path="/order/", user_info=current_user, request=request)


@staff_router.post('/food/{id}/accepted')
def accepted_food(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path=f"/food/{id}/accepted", user_info=current_user,
                             request=request)


@staff_router.post('/food/{id}/pick_up')
def pick_up_food(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path=f"/food/{id}/pick_up", user_info=current_user, request=request)


@staff_router.post('/food/{id}/paid')
def paid_food(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path=f"/food/{id}/paid", user_info=current_user, request=request)


@staff_router.post('/food/{id}/done')
def done_food(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path=f"/food/{id}/done", user_info=current_user, request=request)


@staff_router.post('/food/{id}/cancel')
def cancel_food(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="food", path=f"/food/{id}/cancel", user_info=current_user, request=request)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(staff_router)
