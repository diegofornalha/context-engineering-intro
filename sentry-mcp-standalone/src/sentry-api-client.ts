import fetch from 'node-fetch';

interface SentryAPIConfig {
  authToken: string;
  org: string;
  baseUrl?: string;
}

export class SentryAPIClient {
  private authToken: string;
  private org: string;
  private baseUrl: string;

  constructor(config: SentryAPIConfig) {
    this.authToken = config.authToken;
    this.org = config.org;
    this.baseUrl = config.baseUrl || 'https://sentry.io/api/0';
  }

  private async request(endpoint: string, options: any = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.authToken}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`Sentry API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Projects
  async listProjects() {
    return this.request(`/organizations/${this.org}/projects/`);
  }

  async getProject(projectSlug: string) {
    return this.request(`/projects/${this.org}/${projectSlug}/`);
  }

  async createProject(data: any) {
    return this.request(`/teams/${this.org}/${data.team}/projects/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Issues
  async listIssues(projectSlug: string, query?: string) {
    const params = query ? `?query=${encodeURIComponent(query)}` : '';
    return this.request(`/projects/${this.org}/${projectSlug}/issues/${params}`);
  }

  async getIssue(issueId: string) {
    return this.request(`/issues/${issueId}/`);
  }

  async updateIssue(issueId: string, data: any) {
    return this.request(`/issues/${issueId}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Events
  async listEvents(projectSlug: string) {
    return this.request(`/projects/${this.org}/${projectSlug}/events/`);
  }

  async getEvent(projectSlug: string, eventId: string) {
    return this.request(`/projects/${this.org}/${projectSlug}/events/${eventId}/`);
  }

  // Releases
  async listReleases(projectSlug: string) {
    return this.request(`/projects/${this.org}/${projectSlug}/releases/`);
  }

  async createRelease(version: string, data: any = {}) {
    return this.request(`/organizations/${this.org}/releases/`, {
      method: 'POST',
      body: JSON.stringify({
        version,
        ...data,
      }),
    });
  }

  async getReleaseDetails(version: string) {
    return this.request(`/organizations/${this.org}/releases/${version}/`);
  }

  async deployRelease(version: string, environment: string) {
    return this.request(`/organizations/${this.org}/releases/${version}/deploys/`, {
      method: 'POST',
      body: JSON.stringify({
        environment,
        dateStarted: new Date().toISOString(),
      }),
    });
  }

  // Teams
  async listTeams() {
    return this.request(`/organizations/${this.org}/teams/`);
  }

  async createTeam(name: string, slug: string) {
    return this.request(`/organizations/${this.org}/teams/`, {
      method: 'POST',
      body: JSON.stringify({ name, slug }),
    });
  }

  // Alerts
  async listAlertRules(projectSlug: string) {
    return this.request(`/projects/${this.org}/${projectSlug}/rules/`);
  }

  async createAlertRule(projectSlug: string, rule: any) {
    return this.request(`/projects/${this.org}/${projectSlug}/rules/`, {
      method: 'POST',
      body: JSON.stringify(rule),
    });
  }

  // Organization Stats
  async getOrganizationStats(stat: string, params?: any) {
    const queryParams = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request(`/organizations/${this.org}/stats/${stat}/${queryParams}`);
  }

  // Project Stats
  async getProjectStats(projectSlug: string, stat: string, params?: any) {
    const queryParams = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request(`/projects/${this.org}/${projectSlug}/stats/${stat}/${queryParams}`);
  }

  // Members
  async listMembers() {
    return this.request(`/organizations/${this.org}/members/`);
  }

  async inviteMember(email: string, role: string = 'member') {
    return this.request(`/organizations/${this.org}/members/`, {
      method: 'POST',
      body: JSON.stringify({ email, role }),
    });
  }

  // Integrations
  async listIntegrations() {
    return this.request(`/organizations/${this.org}/integrations/`);
  }

  async getIntegration(integrationId: string) {
    return this.request(`/organizations/${this.org}/integrations/${integrationId}/`);
  }

  // Short ID Resolution
  async resolveShortId(shortId: string) {
    return this.request(`/organizations/${this.org}/shortids/${shortId}/`);
  }

  // Issue Events
  async listIssueEvents(issueId: string) {
    return this.request(`/issues/${issueId}/events/`);
  }

  // Replays
  async listReplays(params?: any) {
    const queryParams = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request(`/organizations/${this.org}/replays/${queryParams}`);
  }

  // Project Keys (DSN)
  async listProjectKeys(projectSlug: string) {
    return this.request(`/projects/${this.org}/${projectSlug}/keys/`);
  }

  async createProjectKey(projectSlug: string, name: string) {
    return this.request(`/projects/${this.org}/${projectSlug}/keys/`, {
      method: 'POST',
      body: JSON.stringify({ name }),
    });
  }

  // Error Events in Project
  async listErrorEventsInProject(projectSlug: string, params?: any) {
    const queryParams = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request(`/projects/${this.org}/${projectSlug}/events/${queryParams}`);
  }

  // Search Errors in File
  async searchErrorsInFile(projectSlug: string, filename: string) {
    const query = `filename:"${filename}"`;
    return this.listIssues(projectSlug, query);
  }
}