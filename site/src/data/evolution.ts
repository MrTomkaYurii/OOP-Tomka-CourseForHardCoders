export type EvolutionStep = {
  lab: number;
  title: string;
  module: string;
  menu: string;
  files: string[];
  concepts: string[];
};

export const evolutionSteps: EvolutionStep[] = [
  {
    lab: 1,
    title: "Основи C#",
    module: "Sandbox",
    menu: "Окремий консольний проєкт",
    files: ["sandbox/intro/Task1.cs ... Task8.cs", "sandbox/intro/Program.cs"],
    concepts: ["базові типи", "умови", "цикли", "static методи", "Console I/O"],
  },
  {
    lab: 2,
    title: "Масиви",
    module: "Sandbox",
    menu: "Окремий консольний проєкт",
    files: ["sandbox/arrays/Task1.cs ... Task8.cs", "sandbox/arrays/Program.cs"],
    concepts: ["T[]", "T[,]", "T[][]", "пошук", "сортування", "2D розклад"],
  },
  {
    lab: 3,
    title: "Класи",
    module: "Catalog",
    menu: "Пацієнти, лікарі, записи, звіт",
    files: ["Patient.cs", "Doctor.cs", "Appointment.cs", "PatientManager.cs", "DoctorManager.cs", "AppointmentManager.cs", "Clinic.cs"],
    concepts: ["class", "constructor", "properties", "ToString()", "масив об'єктів"],
  },
  {
    lab: 4,
    title: "Члени класу",
    module: "Core types",
    menu: "Типи крові, спеціальності, статистика, розклад",
    files: ["Enums/BloodType.cs", "Enums/Speciality.cs", "Enums/AppointmentStatus.cs", "Models/WorkSchedule.cs", "Utils/ClinicFormatter.cs"],
    concepts: ["enum", "struct", "static class", "indexer", "overloading", "out параметр"],
  },
  {
    lab: 5,
    title: "Інкапсуляція",
    module: "Patients+",
    menu: "Валідація і зрозумілі помилки замість падіння",
    files: ["Utils/ClinicValidator.cs", "GrowablePatientManager.cs", "Models/*", "Managers/*"],
    concepts: ["private поля", "явні сеттери", "throw", "try/catch", "namespace"],
  },
  {
    lab: 6,
    title: "Наслідування",
    module: "MedicalRecords",
    menu: "Медична картка",
    files: ["Models/MedicalRecord.cs", "Models/Diagnosis.cs", "Models/LabResult.cs", "Models/Prescription.cs", "Managers/MedicalRecordManager.cs"],
    concepts: ["abstract class", "virtual", "override", "base()", "is/as"],
  },
  {
    lab: 7,
    title: "Інтерфейси",
    module: "Billing",
    menu: "Рахунки",
    files: ["Interfaces/IPayable.cs", "Interfaces/ICancellable.cs", "Interfaces/ISchedulable.cs", "Managers/BillingManager.cs"],
    concepts: ["interface", "кілька інтерфейсів", "контракти поведінки"],
  },
  {
    lab: 8,
    title: "Поліморфізм",
    module: "Appointments+",
    menu: "Внутрішні типи прийомів",
    files: ["Models/RegularAppointment.cs", "Models/UrgentAppointment.cs", "Models/SpecialistAppointment.cs"],
    concepts: ["polymorphism", "override", "sealed", "new method hiding"],
  },
  {
    lab: 9,
    title: "Generics",
    module: "Waiting",
    menu: "Черга очікування",
    files: ["Models/WaitingQueue.cs", "Interfaces/IIdentifiable.cs", "Managers/Repository.cs"],
    concepts: ["List<T>", "Queue<T>", "generic class", "where T : interface"],
  },
  {
    lab: 10,
    title: "Ітератори та компаратори",
    module: "Analytics",
    menu: "Аналітика",
    files: ["Models/DoctorStats.cs", "Models/PatientStats.cs", "Comparators/*", "Managers/AnalyticsManager.cs"],
    concepts: ["IComparable<T>", "IComparer<T>", "IEnumerable<T>", "yield return"],
  },
];
