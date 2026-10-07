using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ClinicApp.Migrations
{
    /// <inheritdoc />
    public partial class AddMedicalRecordsAndOwnedEntities : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "EC_Name",
                table: "Patients",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "EC_Phone",
                table: "Patients",
                type: "nvarchar(20)",
                maxLength: 20,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "EC_Relationship",
                table: "Patients",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: true);

            migrationBuilder.AddColumn<byte[]>(
                name: "RowVersion",
                table: "Patients",
                type: "rowversion",
                rowVersion: true,
                nullable: true);

            migrationBuilder.CreateTable(
                name: "MedicalRecords",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    PatientId = table.Column<int>(type: "int", nullable: false),
                    DoctorId = table.Column<int>(type: "int", nullable: false),
                    Date = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Notes = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false, defaultValue: ""),
                    RecordType = table.Column<string>(type: "nvarchar(13)", maxLength: 13, nullable: false),
                    DiagnosisCode = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: true, defaultValue: ""),
                    Description = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true, defaultValue: ""),
                    IsChronic = table.Column<bool>(type: "bit", nullable: true),
                    TestName = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true, defaultValue: ""),
                    Value = table.Column<double>(type: "float", nullable: true),
                    Unit = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: true, defaultValue: ""),
                    ReferenceRange = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true, defaultValue: ""),
                    IsNormal = table.Column<bool>(type: "bit", nullable: true),
                    MedicationName = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true, defaultValue: ""),
                    Dosage = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true, defaultValue: ""),
                    DurationDays = table.Column<int>(type: "int", nullable: true),
                    Instructions = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true, defaultValue: "")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MedicalRecords", x => x.Id);
                    table.ForeignKey(
                        name: "FK_MedicalRecords_Doctors_DoctorId",
                        column: x => x.DoctorId,
                        principalTable: "Doctors",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_MedicalRecords_Patients_PatientId",
                        column: x => x.PatientId,
                        principalTable: "Patients",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_MedicalRecords_DoctorId",
                table: "MedicalRecords",
                column: "DoctorId");

            migrationBuilder.CreateIndex(
                name: "IX_MedicalRecords_PatientId",
                table: "MedicalRecords",
                column: "PatientId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "MedicalRecords");

            migrationBuilder.DropColumn(
                name: "EC_Name",
                table: "Patients");

            migrationBuilder.DropColumn(
                name: "EC_Phone",
                table: "Patients");

            migrationBuilder.DropColumn(
                name: "EC_Relationship",
                table: "Patients");

            migrationBuilder.DropColumn(
                name: "RowVersion",
                table: "Patients");
        }
    }
}
