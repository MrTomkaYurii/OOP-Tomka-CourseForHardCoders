using ClinicApp.Enums;
using ClinicApp.Models;
using ClinicApp.Utils;

namespace ClinicApp.Managers;

public class TreatmentPlanManager
{
    private readonly List<TreatmentPlan> _plans = new();

    public bool Add(TreatmentPlan plan)
    {
        var validation = ModelValidator.Validate(plan);
        if (!validation.IsValid)
        {
            validation.Print();
            return false;
        }
        _plans.Add(plan);
        return true;
    }

    public TreatmentPlan? GetById(int id) =>
        _plans.FirstOrDefault(p => p.Id == id);

    public TreatmentPlan[] GetByPatient(int patientId) =>
        _plans.Where(p => p.PatientId == patientId).ToArray();

    public TreatmentPlan[] GetByDoctor(int doctorId) =>
        _plans.Where(p => p.DoctorId == doctorId).ToArray();

    public TreatmentPlan[] GetByStatus(TreatmentStatus status) =>
        _plans.Where(p => p.Status == status).ToArray();

    public TreatmentPlan[] GetAll() => _plans.ToArray();
}
