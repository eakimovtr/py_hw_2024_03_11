import uuid

class Employee:
    
    def __init__(self, name: str, rate: float):
        self.name: str = name
        self.rate: float = rate
        self.number: str = str(uuid.uuid4())[:8]
        
    def get_id(self) -> str:
        return self.number
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.number})"


class ProductionWorker(Employee):
    
    # Every new worker is initialized with the object of his shift
    def __init__(self, name: str, rate: float, shift):
        super().__init__(name, rate)
        shift.add_worker(self)

    def get_shift(self) -> int:
        return self.number_of_shift

    def change_shift(self, shift: int) -> None:
        self.number_of_shift = shift if shift in (1, 2) else "Error"

    def day_salary(self) -> float:
        match self.number_of_shift:
            case 1:
                return self.rate * 8
            case 2:
                return self.rate * 8 * 1.5


class ShiftSupervisor(Employee):
    
    def __init__(self, name: str, rate: float):
        super().__init__(name, rate)
        self.shifts: list[Shift] = [] # Supervisor can manage more than one shift
        
    def add_shift(self, shift) -> None:
        if not shift.get_supervisor():
            shift.set_supervisor(self)
            self.shifts.append(shift)
        else:
            raise f"Shift already has a supervisor!"
        
    def remove_shift(self, shift) -> None:
        for s in self.shifts:
            if s == shift:
                self.shifts.remove(s)
        else:
            raise f"Supervisor {self.get_id()} doesn't manage this shift"
    
    def get_shifts(self) -> list[object]:
        return self.shifts
    
    def day_salary(self) -> float:
        return self.rate * 8
    
    def __str__(self) -> str:
        res = "\n-------\n"
        res += f"Shift Supervisor {self.name}. ID: {self.get_id()}\nManaged shifts: {self.get_shifts()}"
        return res
    
        
class Shift:
    
    # There can be only one supervisor for one shift, but many workers (one to many)
    def __init__(self, no: int, supervisor: ShiftSupervisor = None, *workers: ProductionWorker):
        self.__no: int = no
        self.set_supervisor(supervisor)
        self.__workers: list[ProductionWorker] = list(workers)

    def get_no(self) -> int:
        return self.__no
    
    def get_supervisor(self) -> ShiftSupervisor:
        return self.__supervisor
    
    def get_workers(self) -> list[ProductionWorker]:
        return self.__workers
    
    def set_supervisor(self, supervisor: ShiftSupervisor) -> None:
        self.__supervisor = supervisor
    
    def add_worker(self, worker: ProductionWorker) -> None:
        self.__workers.append(worker)
        
    def exclude_worker(self, worker: ProductionWorker) -> None:
        for w in self.__workers:
            if w == worker:
                self.__workers.remove(w)
        else:
            raise f"No such worker on shift {self.get_no()}"
        
    def __repr__(self) -> str:
        return f"Shift {self.get_no()} ( {self.get_supervisor().__repr__()}, {len(self.get_workers())} workers)"
        

# SalaryCalculator is a utility class for computing salary of every employee
class SalaryCalculator:
    periods = ("day", "month", "year")
    
    @classmethod
    def calculate_salary(cls, employee: Employee, period: str) -> float:
        if period not in cls.periods:
            raise f"Wrong time period!"
        if not isinstance(employee, Employee):
            raise f"Unknown employee occupancy, can't calculate salary!"
        
        match period:
            case "day":
                return employee.day_salary()
            case "month":
                return employee.day_salary() * 20
            case "year":
                if isinstance(employee, ProductionWorker):
                    return employee.day_salary() * 240
                if isinstance(employee, ShiftSupervisor):
                    return employee.day_salary() * 240 + cls.calculate_supervisor_bonus(employee)
                
    # Supervisors will have annual bonus for the number of people in their shift
    @staticmethod
    def calculate_supervisor_bonus(supervisor: ShiftSupervisor) -> float:
        bonus_coef = 1000
        workers = 0
        for shift in supervisor.get_shifts():
            workers += len(shift.get_workers())
        
        return workers * bonus_coef


# This is demo class for running simple business simulation and calculate supervisor's salary
class Fabric:
    @staticmethod
    def demo():
        boss_1 = ShiftSupervisor("Big Boss", 8.99)
        boss_2 = ShiftSupervisor("Small Boss", 6.99)

        shift_1 = Shift(1)
        shift_2 = Shift(2)


        ProductionWorker("Lox", 1, shift_1)
        ProductionWorker("Kek", 2.2, shift_1)
        ProductionWorker("Bob", 3, shift_1)
        ProductionWorker("Rob", 1.6, shift_1)

        ProductionWorker("Tom", 3, shift_2)
        ProductionWorker("Jones", 1.5, shift_2)
        ProductionWorker("Katie", 1.8, shift_2)
        
        boss_1.add_shift(shift_1)
        boss_2.add_shift(shift_2)
        
        print(SalaryCalculator.calculate_salary(boss_1, "year"))
        
        
Fabric.demo()