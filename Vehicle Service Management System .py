import json
import os



PRICE_LIST = {
    "Oil Change": 1500,
    "Wheel Alignment": 800,
    "Full Service": 4500,
    "Brake Repair": 2200
}

FILE_NAME = "services.txt"



class ServiceRecord:

    def __init__(self, reg_no, owner, vehicle, service,
                 status="Pending"):

        self.reg_no = reg_no
        self.owner = owner
        self.vehicle = vehicle
        self.service = service
        self.status = status

    
    def calculate_cost(self):
        price = PRICE_LIST[self.service]
        return price * 1.18

    # Display record
    def display(self):
        cost = self.calculate_cost()

        print(
            f"{self.reg_no} | {self.service} | "
            f"Cost incl. 18% GST: Rs. {cost:.2f} | "
            f"Status: {self.status}"
        )

    
    def to_dict(self):
        return {
            "reg_no": self.reg_no,
            "owner": self.owner,
            "vehicle": self.vehicle,
            "service": self.service,
            "status": self.status
        }



services = {}



def load_records():

    global services

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)

            for reg_no, record in data.items():
                services[reg_no] = ServiceRecord(
                    record["reg_no"],
                    record["owner"],
                    record["vehicle"],
                    record["service"],
                    record["status"]
                )

        except (json.JSONDecodeError, KeyError):
            services = {}



def save_records():

    data = {}

    for reg_no, record in services.items():
        data[reg_no] = record.to_dict()

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)



def add_record():

    reg_no = input("Reg no: ").strip().upper()

    if reg_no in services:
        print("Record already exists.")
        return

    owner = input("Owner: ").strip()
    vehicle = input("Vehicle: ").strip()
    service = input("Service: ").strip()

    if service not in PRICE_LIST:
        print(
            "Invalid service type. Choose from: "
            "Oil Change, Wheel Alignment, Full Service, Brake Repair."
        )
        return

    record = ServiceRecord(reg_no, owner, vehicle, service)

    services[reg_no] = record
    save_records()

    print("Record added.", end=" ")
    record.display()



def view_records():

    if not services:
        print("No records found.")
        return

    for record in services.values():
        record.display()



def update_status():

    reg_no = input("Reg no: ").strip().upper()

    if reg_no not in services:
        print(f"No record found for {reg_no}.")
        return

    new_status = input("New status: ").strip().title()

    valid_status = ["Pending", "In Progress", "Completed"]

    if new_status not in valid_status:
        print("Invalid status.")
        return

    old_status = services[reg_no].status

    services[reg_no].status = new_status

    save_records()

    print(f"Status updated: {old_status} -> {new_status}")



def delete_record():

    reg_no = input("Reg no: ").strip().upper()

    if reg_no not in services:
        print(f"No record found for {reg_no}.")
        return

    del services[reg_no]

    save_records()

    print(f"Record for {reg_no} deleted.")



def main():

    load_records()

    while True:

        print("\n===== VEHICLE SERVICE MANAGEMENT SYSTEM =====")
        print("1. Add record")
        print("2. View records")
        print("3. Update status")
        print("4. Delete record")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_record()

        elif choice == "2":
            view_records()

        elif choice == "3":
            update_status()

        elif choice == "4":
            delete_record()

        elif choice == "5":
            print("Thank you for using Vehicle Service Management System.")
            break

        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
    
