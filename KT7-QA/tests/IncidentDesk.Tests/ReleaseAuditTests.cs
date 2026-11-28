using IncidentDesk;

namespace IncidentDesk.Tests;

public class ReleaseAuditTests
{
    [Fact]
    public void Reporter_list_does_not_contain_another_authors_incident()
    {
        var desk = new IncidentDeskService();

        var reporterA = new User("reporter-a", "alpha", Role.Reporter);
        var reporterB = new User("reporter-b", "alpha", Role.Reporter);

        var ownIncident = desk.Create(reporterA, "Own incident", Severity.Normal);
        var anotherIncident = desk.Create(reporterB, "Another incident", Severity.Critical);

        var incidents = desk.List(reporterA);

        Assert.Contains(incidents, item => item.Id == ownIncident.Id);
        Assert.DoesNotContain(incidents, item => item.Id == anotherIncident.Id);
    }

    [Fact]
    public void Auditor_cannot_close_an_incident_and_incident_remains_unchanged()
    {
        var desk = new IncidentDeskService();

        var reporter = new User("reporter-a", "alpha", Role.Reporter);
        var auditor = new User("auditor", "audit", Role.Auditor);

        var incident = desk.Create(reporter, "Payment outage", Severity.Critical);

        Assert.Throws<AccessDeniedException>(
            () => desk.Close(auditor, incident.Id));

        var storedIncident = desk.Get(auditor, incident.Id);

        Assert.Equal(incident, storedIncident);
        Assert.Equal(IncidentStatus.New, storedIncident.Status);
    }

    [Fact]
    public void Reporter_cannot_rename_an_incident_after_work_has_started()
    {
        var desk = new IncidentDeskService();

        var reporter = new User("reporter-a", "alpha", Role.Reporter);
        var coordinator = new User("coordinator-a", "alpha", Role.Coordinator);
        var responder = new User("responder-a", "alpha", Role.Responder);

        var incident = desk.Create(reporter, "Original title", Severity.Normal);

        desk.Assign(coordinator, incident.Id, responder);
        desk.Start(responder, incident.Id);

        Assert.Throws<InvalidIncidentStateException>(
            () => desk.Rename(reporter, incident.Id, "Changed title"));

        var storedIncident = desk.Get(reporter, incident.Id);

        Assert.Equal("Original title", storedIncident.Title);
        Assert.Equal(IncidentStatus.InProgress, storedIncident.Status);
    }

    [Fact]
    public void Reporter_cannot_get_another_authors_incident_in_the_same_team()
    {
        var desk = new IncidentDeskService();

        var reporterA = new User("reporter-a", "alpha", Role.Reporter);
        var reporterB = new User("reporter-b", "alpha", Role.Reporter);

        var anotherIncident = desk.Create(
            reporterB, "Another author's incident", Severity.Normal);

        Assert.Throws<AccessDeniedException>(
            () => desk.Get(reporterA, anotherIncident.Id));
    }
}
