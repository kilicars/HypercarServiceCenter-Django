from django.views import View
from django.shortcuts import render, redirect
from _collections import deque

service_id = 0;
next_service_id = None

service_types = {
    "CO": "change_oil",
    "IT": "inflate_tires",
    "DG": "diagnostic"
}

line_of_cars = {
    service_types["CO"]: deque(),
    service_types["IT"]: deque(),
    service_types["DG"]: deque()
}


class WelcomeView(View):
    def get(self, request):
        return render(request, "tickets/welcome.html")


class MainMenuView(View):
    def get(self, request):
        return render(request, "tickets/main_menu.html")


class MenuView(View):
    menu_choices = {
        service_types["CO"]: "Change Oil",
        service_types["IT"]: "Inflate tires",
        service_types["DG"]: "Diagnostic"
    }

    def get(self, request):
        return render(request, "tickets/service_menu.html", {"menu_choices": self.menu_choices})


class TicketView(View):
    def get(self, request, service_type):
        global service_id
        service_id += 1
        waiting_time = len(line_of_cars[service_types["CO"]]) * 2

        if service_type == service_types["IT"]:
            waiting_time = len(line_of_cars[service_types["CO"]]) * 2 + \
                           len(line_of_cars[service_types["IT"]]) * 5

        elif service_type == service_types["DG"]:
            waiting_time = len(line_of_cars[service_types["CO"]]) * 2 + \
                           len(line_of_cars[service_types["IT"]]) * 5 + \
                           len(line_of_cars[service_types["DG"]]) * 30

        line_of_cars[service_type].appendleft(service_id)

        context = {"service_id": service_id, "waiting_time": waiting_time}
        return render(request, "tickets/serve.html", context=context)


class ProcessView(View):
    def get(self, request):
        oil_line_count = len(line_of_cars[service_types["CO"]])
        tire_line_count = len(line_of_cars[service_types["IT"]])
        diagnostic_line_count = len(line_of_cars[service_types["DG"]])
        context = {"oil_line_count": oil_line_count,
                   "tire_line_count": tire_line_count,
                   "diagnostic_line_count": diagnostic_line_count}
        return render(request, "tickets/process.html", context=context)

    def post(self, request):
        global next_service_id

        if len(line_of_cars[service_types["CO"]]) > 0:
            next_service_id = line_of_cars[service_types["CO"]].pop()
        elif len(line_of_cars[service_types["IT"]]) > 0:
            next_service_id = line_of_cars[service_types["IT"]].pop()
        elif len(line_of_cars[service_types["DG"]]) > 0:
            next_service_id = line_of_cars[service_types["DG"]].pop()
        else:
            next_service_id = None

        return redirect('/next')


class NextCustomerView(View):
    def get(self, request):
        global next_service_id
        context = {"next_service_id": next_service_id}
        return render(request, "tickets/next.html", context=context)
