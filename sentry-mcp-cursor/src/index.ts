#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from "@modelcontextprotocol/sdk/types.js";
import * as Sentry from "@sentry/node";
import { SentryAPIClient } from "./sentry-api-client.js";

// Server configuration interface
interface SentryConfig {
  dsn?: string;
  environment?: string;
  release?: string;
  tracesSampleRate?: number;
  debug?: boolean;
}

// Initialize Sentry from environment or provided config
function initializeSentry(config?: SentryConfig) {
  const sentryConfig = {
    dsn: config?.dsn || process.env.SENTRY_DSN,
    environment: config?.environment || process.env.NODE_ENV || "development",
    release: config?.release || process.env.SENTRY_RELEASE,
    tracesSampleRate: config?.tracesSampleRate || 1.0,
    debug: config?.debug || false,
  };

  if (!sentryConfig.dsn) {
    console.warn("Sentry DSN not provided. Sentry will not be initialized.");
    return false;
  }

  Sentry.init(sentryConfig);
  return true;
}

// Parse command line arguments for Sentry config
const args = process.argv.slice(2);
const config: SentryConfig = {};

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--dsn":
      config.dsn = args[++i];
      break;
    case "--environment":
      config.environment = args[++i];
      break;
    case "--release":
      config.release = args[++i];
      break;
    case "--debug":
      config.debug = true;
      break;
  }
}

// Initialize Sentry
const sentryInitialized = initializeSentry(config);

// Initialize Sentry API Client
let apiClient: SentryAPIClient | null = null;
const authToken = process.env.SENTRY_AUTH_TOKEN || args.find((arg, i) => args[i - 1] === '--auth-token');
const org = process.env.SENTRY_ORG || args.find((arg, i) => args[i - 1] === '--org') || 'coflow';

if (authToken && typeof authToken === 'string') {
  apiClient = new SentryAPIClient({
    authToken,
    org,
    baseUrl: process.env.SENTRY_API_URL,
  });
  console.error("Sentry API client initialized for organization:", org);
}

// Create server instance
const server = new Server(
  {
    name: "mcp-sentry",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "sentry_capture_exception",
        description: "Capture and send an exception to Sentry",
        inputSchema: {
          type: "object",
          properties: {
            error: {
              type: "string",
              description: "Error message or description",
            },
            level: {
              type: "string",
              enum: ["fatal", "error", "warning", "info", "debug"],
              description: "Severity level of the error",
              default: "error",
            },
            tags: {
              type: "object",
              description: "Key-value pairs to tag the error",
              additionalProperties: { type: "string" },
            },
            context: {
              type: "object",
              description: "Additional context data",
              additionalProperties: true,
            },
            user: {
              type: "object",
              description: "User information",
              properties: {
                id: { type: "string" },
                email: { type: "string" },
                username: { type: "string" },
              },
            },
          },
          required: ["error"],
        },
      },
      {
        name: "sentry_capture_message",
        description: "Capture and send a message to Sentry",
        inputSchema: {
          type: "object",
          properties: {
            message: {
              type: "string",
              description: "Message to send to Sentry",
            },
            level: {
              type: "string",
              enum: ["fatal", "error", "warning", "info", "debug"],
              description: "Severity level of the message",
              default: "info",
            },
            tags: {
              type: "object",
              description: "Key-value pairs to tag the message",
              additionalProperties: { type: "string" },
            },
            context: {
              type: "object",
              description: "Additional context data",
              additionalProperties: true,
            },
          },
          required: ["message"],
        },
      },
      {
        name: "sentry_add_breadcrumb",
        description: "Add a breadcrumb for debugging context",
        inputSchema: {
          type: "object",
          properties: {
            message: {
              type: "string",
              description: "Breadcrumb message",
            },
            category: {
              type: "string",
              description: "Category of the breadcrumb",
            },
            level: {
              type: "string",
              enum: ["fatal", "error", "warning", "info", "debug"],
              description: "Severity level",
              default: "info",
            },
            data: {
              type: "object",
              description: "Additional data for the breadcrumb",
              additionalProperties: true,
            },
          },
          required: ["message"],
        },
      },
      {
        name: "sentry_set_user",
        description: "Set user context for Sentry",
        inputSchema: {
          type: "object",
          properties: {
            id: {
              type: "string",
              description: "User ID",
            },
            email: {
              type: "string",
              description: "User email",
            },
            username: {
              type: "string",
              description: "Username",
            },
            ip_address: {
              type: "string",
              description: "User IP address",
            },
            segment: {
              type: "string",
              description: "User segment",
            },
          },
        },
      },
      {
        name: "sentry_set_tag",
        description: "Set a tag that will be sent with all events",
        inputSchema: {
          type: "object",
          properties: {
            key: {
              type: "string",
              description: "Tag key",
            },
            value: {
              type: "string",
              description: "Tag value",
            },
          },
          required: ["key", "value"],
        },
      },
      {
        name: "sentry_set_context",
        description: "Set custom context data",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "Context name",
            },
            context: {
              type: "object",
              description: "Context data",
              additionalProperties: true,
            },
          },
          required: ["name", "context"],
        },
      },
      {
        name: "sentry_start_transaction",
        description: "Start a performance monitoring transaction",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "Transaction name",
            },
            op: {
              type: "string",
              description: "Operation type (e.g., 'http.request', 'db.query')",
            },
            description: {
              type: "string",
              description: "Transaction description",
            },
          },
          required: ["name", "op"],
        },
      },
      {
        name: "sentry_finish_transaction",
        description: "Finish the current transaction",
        inputSchema: {
          type: "object",
          properties: {
            status: {
              type: "string",
              description: "Transaction status",
              enum: ["ok", "cancelled", "unknown", "invalid_argument", "deadline_exceeded", "not_found", "already_exists", "permission_denied", "resource_exhausted", "failed_precondition", "aborted", "out_of_range", "unimplemented", "internal_error", "unavailable", "data_loss", "unauthenticated"],
              default: "ok",
            },
          },
        },
      },
      {
        name: "sentry_start_session",
        description: "Start a new session for release health monitoring",
        inputSchema: {
          type: "object",
          properties: {
            distinctId: {
              type: "string",
              description: "Unique user identifier (ID, email, or username)",
            },
            sessionId: {
              type: "string",
              description: "Optional custom session ID",
            },
            release: {
              type: "string",
              description: "Release version",
            },
            environment: {
              type: "string",
              description: "Environment name (production, staging, etc)",
            },
          },
        },
      },
      {
        name: "sentry_end_session",
        description: "End the current session with a specific status",
        inputSchema: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["exited", "crashed", "abnormal", "errored"],
              description: "How the session ended",
              default: "exited",
            },
          },
        },
      },
      {
        name: "sentry_set_release",
        description: "Set the release version for release health tracking",
        inputSchema: {
          type: "object",
          properties: {
            release: {
              type: "string",
              description: "Release version (e.g., 'myapp@1.0.0')",
            },
            dist: {
              type: "string",
              description: "Distribution identifier",
            },
          },
          required: ["release"],
        },
      },
      {
        name: "sentry_capture_session",
        description: "Manually capture a session for server-mode/request-mode",
        inputSchema: {
          type: "object",
          properties: {
            sessionId: {
              type: "string",
              description: "Unique session identifier",
            },
            distinctId: {
              type: "string",
              description: "User identifier",
            },
            status: {
              type: "string",
              enum: ["ok", "exited", "crashed", "abnormal", "errored"],
              description: "Session status",
              default: "ok",
            },
            duration: {
              type: "number",
              description: "Session duration in seconds",
            },
            errors: {
              type: "number",
              description: "Number of errors in session",
              default: 0,
            },
          },
          required: ["sessionId"],
        },
      },
      // API Management Tools
      {
        name: "sentry_list_projects",
        description: "List all projects in the organization",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "sentry_list_issues",
        description: "List issues for a project",
        inputSchema: {
          type: "object",
          properties: {
            projectSlug: {
              type: "string",
              description: "Project slug/identifier",
            },
            query: {
              type: "string",
              description: "Search query (e.g., 'is:unresolved', 'level:error')",
            },
          },
          required: ["projectSlug"],
        },
      },
      {
        name: "sentry_create_release",
        description: "Create a new release",
        inputSchema: {
          type: "object",
          properties: {
            version: {
              type: "string",
              description: "Release version (e.g., 'myapp@1.0.0')",
            },
            projects: {
              type: "array",
              items: { type: "string" },
              description: "List of project slugs",
            },
            url: {
              type: "string",
              description: "Release URL",
            },
            dateReleased: {
              type: "string",
              description: "Release date (ISO format)",
            },
          },
          required: ["version"],
        },
      },
      {
        name: "sentry_list_releases",
        description: "List releases for a project",
        inputSchema: {
          type: "object",
          properties: {
            projectSlug: {
              type: "string",
              description: "Project slug/identifier",
            },
          },
          required: ["projectSlug"],
        },
      },
      {
        name: "sentry_get_organization_stats",
        description: "Get organization statistics",
        inputSchema: {
          type: "object",
          properties: {
            stat: {
              type: "string",
              enum: ["received", "rejected", "blacklisted"],
              description: "Type of statistic",
            },
            since: {
              type: "string",
              description: "Start date (ISO format or timestamp)",
            },
            until: {
              type: "string",
              description: "End date (ISO format or timestamp)",
            },
            resolution: {
              type: "string",
              enum: ["10s", "1h", "1d"],
              description: "Time resolution",
            },
          },
          required: ["stat"],
        },
      },
      {
        name: "sentry_create_alert_rule",
        description: "Create an alert rule for a project",
        inputSchema: {
          type: "object",
          properties: {
            projectSlug: {
              type: "string",
              description: "Project slug/identifier",
            },
            name: {
              type: "string",
              description: "Alert rule name",
            },
            conditions: {
              type: "array",
              description: "Alert conditions",
            },
            actions: {
              type: "array",
              description: "Alert actions",
            },
            frequency: {
              type: "number",
              description: "Check frequency in minutes",
              default: 30,
            },
          },
          required: ["projectSlug", "name"],
        },
      },
      {
        name: "sentry_resolve_short_id",
        description: "Retrieve details about an issue using its short ID. Maps short IDs to issue details, project context and status.",
        inputSchema: {
          type: "object",
          properties: {
            shortId: {
              type: "string",
              description: "The short ID of the issue (e.g., 'PROJ-123')",
            },
          },
          required: ["shortId"],
        },
      },
      {
        name: "sentry_get_event",
        description: "Retrieve a specific Sentry event from an issue. Requires issue ID/URL and event ID.",
        inputSchema: {
          type: "object",
          properties: {
            projectSlug: {
              type: "string",
              description: "Project slug/identifier",
            },
            eventId: {
              type: "string",
              description: "Event ID",
            },
          },
          required: ["projectSlug", "eventId"],
        },
      },
      {
        name: "sentry_list_error_events_in_project",
        description: "List error events from a specific Sentry project. View recent errors, frequency patterns and occurrence timestamps.",
        inputSchema: {
          type: "object",
          properties: {
            projectSlug: {
              type: "string",
              description: "Project slug/identifier",
            },
            limit: {
              type: "number",
              description: "Number of events to return",
              default: 50,
            },
            query: {
              type: "string",
              description: "Search query",
            },
          },
          required: ["projectSlug"],
        },
      },
      {
        name: "sentry_create_project",
        description: "Create a new project in Sentry. Track deployments, releases and health metrics.",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "Project name",
            },
            slug: {
              type: "string",
              description: "Project slug (URL-friendly identifier)",
            },
            platform: {
              type: "string",
              description: "Platform (e.g., 'javascript', 'python', 'node')",
            },
            team: {
              type: "string",
              description: "Team slug",
            },
          },
          required: ["name", "slug", "team"],
        },
      },
      {
        name: "sentry_list_issue_events",
        description: "List events for a specific Sentry issue. Analyze event details, metadata and patterns.",
        inputSchema: {
          type: "object",
          properties: {
            issueId: {
              type: "string",
              description: "Issue ID",
            },
            limit: {
              type: "number",
              description: "Number of events to return",
              default: 50,
            },
          },
          required: ["issueId"],
        },
      },
      {
        name: "sentry_get_issue",
        description: "Retrieve and analyze a Sentry issue. Accepts issue URL or ID.",
        inputSchema: {
          type: "object",
          properties: {
            issueId: {
              type: "string",
              description: "Issue ID or URL",
            },
          },
          required: ["issueId"],
        },
      },
      {
        name: "sentry_list_organization_replays",
        description: "List replays from a Sentry organization. Monitor user sessions, interactions, errors and experience issues.",
        inputSchema: {
          type: "object",
          properties: {
            project: {
              type: "string",
              description: "Project ID or slug",
            },
            limit: {
              type: "number",
              description: "Number of replays to return",
              default: 50,
            },
            query: {
              type: "string",
              description: "Search query",
            },
          },
          required: [],
        },
      },
      {
        name: "sentry_setup_project",
        description: "Set up Sentry for a project returning a DSN and instructions for setup.",
        inputSchema: {
          type: "object",
          properties: {
            projectSlug: {
              type: "string",
              description: "Project slug/identifier",
            },
            platform: {
              type: "string",
              description: "Platform for installation instructions",
              default: "javascript",
            },
          },
          required: ["projectSlug"],
        },
      },
      {
        name: "sentry_search_errors_in_file",
        description: "Search for Sentry errors occurring in a specific file. Find all issues related to a particular file path or filename.",
        inputSchema: {
          type: "object",
          properties: {
            projectSlug: {
              type: "string",
              description: "Project slug/identifier",
            },
            filename: {
              type: "string",
              description: "File path or filename to search for",
            },
          },
          required: ["projectSlug", "filename"],
        },
      },
    ],
  };
});

// Map severity levels
function mapSeverityLevel(level: string): Sentry.SeverityLevel {
  const severityMap: Record<string, Sentry.SeverityLevel> = {
    fatal: "fatal",
    error: "error",
    warning: "warning",
    info: "info",
    debug: "debug",
  };
  return severityMap[level] || "error";
}

// Current transaction storage
let currentTransaction: any | null = null;

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (!sentryInitialized) {
    throw new McpError(
      ErrorCode.InternalError,
      "Sentry is not initialized. Please provide a DSN."
    );
  }

  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "sentry_capture_exception": {
        const { error, level = "error", tags, context, user } = args as any;
        
        // Create an Error object if string provided
        const errorObj = error instanceof Error ? error : new Error(error);
        
        // Create a new scope for this specific error
        Sentry.withScope((scope) => {
          scope.setLevel(mapSeverityLevel(level));
          
          if (tags) {
            Object.entries(tags).forEach(([key, value]) => {
              scope.setTag(key, value as string);
            });
          }
          
          if (context) {
            Object.entries(context).forEach(([key, value]) => {
              scope.setContext(key, value as any);
            });
          }
          
          if (user) {
            scope.setUser(user);
          }
          
          Sentry.captureException(errorObj);
        });
        
        return {
          content: [
            {
              type: "text",
              text: `Exception captured: ${error}`,
            },
          ],
        };
      }
      
      case "sentry_capture_message": {
        const { message, level = "info", tags, context } = args as any;
        
        Sentry.withScope((scope) => {
          scope.setLevel(mapSeverityLevel(level));
          
          if (tags) {
            Object.entries(tags).forEach(([key, value]) => {
              scope.setTag(key, value as string);
            });
          }
          
          if (context) {
            Object.entries(context).forEach(([key, value]) => {
              scope.setContext(key, value as any);
            });
          }
          
          Sentry.captureMessage(message, mapSeverityLevel(level));
        });
        
        return {
          content: [
            {
              type: "text",
              text: `Message captured: ${message}`,
            },
          ],
        };
      }
      
      case "sentry_add_breadcrumb": {
        const { message, category, level = "info", data } = args as any;
        
        Sentry.addBreadcrumb({
          message,
          category,
          level: mapSeverityLevel(level),
          data,
          timestamp: Date.now() / 1000,
        });
        
        return {
          content: [
            {
              type: "text",
              text: `Breadcrumb added: ${message}`,
            },
          ],
        };
      }
      
      case "sentry_set_user": {
        const userInfo = args as any;
        Sentry.setUser(userInfo);
        
        return {
          content: [
            {
              type: "text",
              text: `User context set: ${JSON.stringify(userInfo)}`,
            },
          ],
        };
      }
      
      case "sentry_set_tag": {
        const { key, value } = args as any;
        Sentry.setTag(key, value);
        
        return {
          content: [
            {
              type: "text",
              text: `Tag set: ${key}=${value}`,
            },
          ],
        };
      }
      
      case "sentry_set_context": {
        const { name: contextName, context } = args as any;
        Sentry.setContext(contextName, context);
        
        return {
          content: [
            {
              type: "text",
              text: `Context set: ${contextName}`,
            },
          ],
        };
      }
      
      case "sentry_start_transaction": {
        const { name: transactionName, op, description } = args as any;
        
        if (currentTransaction) {
          currentTransaction.end();
        }
        
        currentTransaction = Sentry.startSpan(
          { name: transactionName, op },
          () => {
            // Transaction is active here
            return null;
          }
        );
        
        return {
          content: [
            {
              type: "text",
              text: `Transaction started: ${transactionName} (${op})`,
            },
          ],
        };
      }
      
      case "sentry_finish_transaction": {
        const { status = "ok" } = args as any;
        
        if (!currentTransaction) {
          throw new Error("No active transaction to finish");
        }
        
        currentTransaction.end();
        currentTransaction = null;
        
        return {
          content: [
            {
              type: "text",
              text: `Transaction finished with status: ${status}`,
            },
          ],
        };
      }
      
      case "sentry_start_session": {
        const { distinctId, sessionId, release, environment } = args as any;
        
        // Start a new session
        const sessionData: any = {
          release,
          environment,
        };
        
        if (distinctId) {
          Sentry.setUser({ id: distinctId });
        }
        
        Sentry.startSession(sessionData);
        
        return {
          content: [
            {
              type: "text",
              text: `Session started${sessionId ? ` with ID: ${sessionId}` : ''}`,
            },
          ],
        };
      }
      
      case "sentry_end_session": {
        const { status = "exited" } = args as any;
        
        // End the current session
        Sentry.endSession();
        
        // If status is crashed or abnormal, capture it
        if (status === "crashed") {
          Sentry.captureException(new Error("Session ended with crash"));
        } else if (status === "abnormal") {
          Sentry.captureMessage("Session ended abnormally", "warning");
        }
        
        return {
          content: [
            {
              type: "text",
              text: `Session ended with status: ${status}`,
            },
          ],
        };
      }
      
      case "sentry_set_release": {
        const { release, dist } = args as any;
        
        // Set release globally
        Sentry.setTag("release", release);
        if (dist) {
          Sentry.setTag("dist", dist);
        }
        
        return {
          content: [
            {
              type: "text",
              text: `Release set to: ${release}${dist ? ` (dist: ${dist})` : ''}`,
            },
          ],
        };
      }
      
      case "sentry_capture_session": {
        const { sessionId, distinctId, status = "ok", duration, errors = 0 } = args as any;
        
        // Capture session data manually (useful for server-mode)
        const sessionData = {
          sid: sessionId,
          did: distinctId,
          status,
          duration,
          errors,
          timestamp: Date.now() / 1000,
          attrs: {
            release: config.release,
            environment: config.environment || "production",
          },
        };
        
        // Log session for monitoring
        Sentry.addBreadcrumb({
          category: "session",
          message: `Session ${sessionId} captured`,
          level: "info",
          data: sessionData,
        });
        
        return {
          content: [
            {
              type: "text",
              text: `Session captured: ${sessionId} (status: ${status}, duration: ${duration}s, errors: ${errors})`,
            },
          ],
        };
      }
      
      // API Management Tools
      case "sentry_list_projects": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const projects = await apiClient.listProjects();
        
        return {
          content: [
            {
              type: "text",
              text: `Found ${projects.length} projects:\n${projects.map((p: any) => `- ${p.slug}: ${p.name}`).join('\n')}`,
            },
          ],
        };
      }
      
      case "sentry_list_issues": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { projectSlug, query } = args as any;
        const issues = await apiClient.listIssues(projectSlug, query);
        
        return {
          content: [
            {
              type: "text",
              text: `Found ${issues.length} issues in ${projectSlug}:\n${issues.slice(0, 10).map((i: any) => 
                `- [${i.level}] ${i.title} (${i.count} events)`
              ).join('\n')}${issues.length > 10 ? '\n... and more' : ''}`,
            },
          ],
        };
      }
      
      case "sentry_create_release": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { version, projects, url, dateReleased } = args as any;
        const release = await apiClient.createRelease(version, {
          projects,
          url,
          dateReleased: dateReleased || new Date().toISOString(),
        });
        
        return {
          content: [
            {
              type: "text",
              text: `Release created: ${release.version}\nProjects: ${release.projects?.join(', ') || 'none'}`,
            },
          ],
        };
      }
      
      case "sentry_list_releases": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { projectSlug } = args as any;
        const releases = await apiClient.listReleases(projectSlug);
        
        return {
          content: [
            {
              type: "text",
              text: `Found ${releases.length} releases:\n${releases.slice(0, 10).map((r: any) => 
                `- ${r.version} (${new Date(r.dateCreated).toLocaleDateString()})`
              ).join('\n')}${releases.length > 10 ? '\n... and more' : ''}`,
            },
          ],
        };
      }
      
      case "sentry_get_organization_stats": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { stat, since, until, resolution } = args as any;
        const stats = await apiClient.getOrganizationStats(stat, {
          since,
          until,
          resolution,
        });
        
        return {
          content: [
            {
              type: "text",
              text: `Organization ${stat} stats:\n${JSON.stringify(stats, null, 2)}`,
            },
          ],
        };
      }
      
      case "sentry_create_alert_rule": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { projectSlug, name, conditions = [], actions = [], frequency } = args as any;
        
        // Default alert rule if not provided
        const rule = {
          name,
          conditions: conditions.length > 0 ? conditions : [
            {
              id: 'sentry.rules.conditions.first_seen_event.FirstSeenEventCondition',
            }
          ],
          actions: actions.length > 0 ? actions : [
            {
              id: 'sentry.rules.actions.notify_event.NotifyEventAction',
            }
          ],
          actionMatch: 'all',
          frequency: frequency || 30,
        };
        
        const createdRule = await apiClient.createAlertRule(projectSlug, rule);
        
        return {
          content: [
            {
              type: "text",
              text: `Alert rule created: ${createdRule.name} for project ${projectSlug}`,
            },
          ],
        };
      }

      case "sentry_resolve_short_id": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { shortId } = args as any;
        const result = await apiClient.resolveShortId(shortId);
        
        return {
          content: [
            {
              type: "text",
              text: `Issue resolved from short ID ${shortId}:\n` +
                `- Issue ID: ${result.groupId}\n` +
                `- Project: ${result.projectSlug}\n` +
                `- Organization: ${result.organizationSlug}\n` +
                `- Title: ${result.group.metadata.title}\n` +
                `- Status: ${result.group.status}\n` +
                `- Level: ${result.group.level}\n` +
                `- First seen: ${result.group.firstSeen}\n` +
                `- Last seen: ${result.group.lastSeen}`,
            },
          ],
        };
      }

      case "sentry_get_event": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { projectSlug, eventId } = args as any;
        const event = await apiClient.getEvent(projectSlug, eventId);
        
        return {
          content: [
            {
              type: "text",
              text: `Event ${eventId} details:\n` +
                `- Title: ${event.title}\n` +
                `- Message: ${event.message}\n` +
                `- Platform: ${event.platform}\n` +
                `- Date: ${event.dateCreated}\n` +
                `- User: ${event.user ? JSON.stringify(event.user) : 'N/A'}\n` +
                `- Tags: ${JSON.stringify(event.tags)}`,
            },
          ],
        };
      }

      case "sentry_list_error_events_in_project": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { projectSlug, limit = 50, query } = args as any;
        const events = await apiClient.listErrorEventsInProject(projectSlug, { limit, query });
        
        return {
          content: [
            {
              type: "text",
              text: `Found ${events.length} error events in project ${projectSlug}:\n` +
                events.map((e: any) => `- ${e.title} (${e.eventID}) - ${e.dateCreated}`).join('\n'),
            },
          ],
        };
      }

      case "sentry_create_project": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { name, slug, platform = "javascript", team } = args as any;
        const project = await apiClient.createProject({ name, slug, platform, team });
        
        return {
          content: [
            {
              type: "text",
              text: `Project created successfully:\n` +
                `- Name: ${project.name}\n` +
                `- Slug: ${project.slug}\n` +
                `- ID: ${project.id}\n` +
                `- Platform: ${project.platform}\n` +
                `- Status: ${project.status}`,
            },
          ],
        };
      }

      case "sentry_list_issue_events": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { issueId, limit = 50 } = args as any;
        const events = await apiClient.listIssueEvents(issueId);
        
        return {
          content: [
            {
              type: "text",
              text: `Found ${events.length} events for issue ${issueId}:\n` +
                events.slice(0, limit).map((e: any) => 
                  `- ${e.eventID} - ${e.dateCreated} - ${e.message || e.title}`
                ).join('\n'),
            },
          ],
        };
      }

      case "sentry_get_issue": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { issueId } = args as any;
        const issue = await apiClient.getIssue(issueId);
        
        return {
          content: [
            {
              type: "text",
              text: `Issue ${issueId} details:\n` +
                `- Title: ${issue.title}\n` +
                `- Short ID: ${issue.shortId}\n` +
                `- Status: ${issue.status}\n` +
                `- Level: ${issue.level}\n` +
                `- Platform: ${issue.platform || 'N/A'}\n` +
                `- First seen: ${issue.firstSeen}\n` +
                `- Last seen: ${issue.lastSeen}\n` +
                `- Event count: ${issue.count}\n` +
                `- User count: ${issue.userCount}`,
            },
          ],
        };
      }

      case "sentry_list_organization_replays": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { project, limit = 50, query } = args as any;
        const params: any = { limit };
        if (project) params.project = project;
        if (query) params.query = query;
        
        const replays = await apiClient.listReplays(params);
        
        return {
          content: [
            {
              type: "text",
              text: `Found ${replays.length} replays:\n` +
                replays.map((r: any) => 
                  `- ${r.id} - ${r.user?.email || 'anonymous'} - ${r.started_at} - ${r.duration}s`
                ).join('\n'),
            },
          ],
        };
      }

      case "sentry_setup_project": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { projectSlug, platform = "javascript" } = args as any;
        
        // Get project keys (DSN)
        const keys = await apiClient.listProjectKeys(projectSlug);
        let dsn = '';
        
        if (keys.length > 0) {
          dsn = keys[0].dsn.public;
        } else {
          // Create a new key if none exists
          const newKey = await apiClient.createProjectKey(projectSlug, 'Default');
          dsn = newKey.dsn.public;
        }
        
        // Installation instructions based on platform
        const instructions: { [key: string]: string } = {
          javascript: `// Install Sentry
npm install --save @sentry/browser

// Initialize Sentry
import * as Sentry from "@sentry/browser";

Sentry.init({
  dsn: "${dsn}",
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});`,
          node: `// Install Sentry
npm install --save @sentry/node

// Initialize Sentry
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: "${dsn}",
  tracesSampleRate: 1.0,
});`,
          python: `# Install Sentry
pip install --upgrade sentry-sdk

# Initialize Sentry
import sentry_sdk

sentry_sdk.init(
    dsn="${dsn}",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)`,
        };
        
        return {
          content: [
            {
              type: "text",
              text: `Sentry setup for project ${projectSlug}:\n\n` +
                `DSN: ${dsn}\n\n` +
                `Installation instructions for ${platform}:\n\n` +
                (instructions[platform] || instructions.javascript),
            },
          ],
        };
      }

      case "sentry_search_errors_in_file": {
        if (!apiClient) {
          throw new Error("Sentry API client not initialized. Provide auth token.");
        }
        
        const { projectSlug, filename } = args as any;
        const issues = await apiClient.searchErrorsInFile(projectSlug, filename);
        
        return {
          content: [
            {
              type: "text",
              text: `Found ${issues.length} issues in file ${filename}:\n` +
                issues.map((i: any) => 
                  `- ${i.shortId}: ${i.title} (${i.count} events, ${i.userCount} users)`
                ).join('\n'),
            },
          ],
        };
      }
      
      default:
        throw new McpError(
          ErrorCode.MethodNotFound,
          `Unknown tool: ${name}`
        );
    }
  } catch (error) {
    throw new McpError(
      ErrorCode.InternalError,
      error instanceof Error ? error.message : String(error)
    );
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP Sentry server running on stdio");
}

main().catch((error) => {
  console.error("Failed to start server:", error);
  process.exit(1);
});