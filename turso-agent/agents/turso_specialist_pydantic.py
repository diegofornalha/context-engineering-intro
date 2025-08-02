#!/usr/bin/env python3
"""
Turso Specialist Agent - Versão PydanticAI
Implementação correta seguindo padrões PydanticAI para o PRP ID 6
"""

import asyncio
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import subprocess
import requests

# PydanticAI imports
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.test import TestModel
from dataclasses import dataclass
from pydantic import BaseModel, Field

# Local imports
from ..config.turso_settings import TursoSettings
from ..tools.turso_manager import TursoManager
from ..tools.mcp_integrator import MCPTursoIntegrator

@dataclass
class TursoAgentDependencies:
    """Dependencies for Turso Specialist Agent - PydanticAI pattern"""
    turso_api_token: str
    turso_organization: str
    default_database: Optional[str] = None
    session_id: Optional[str] = None
    enable_mcp_integration: bool = True
    debug_mode: bool = False

class TursoQueryRequest(BaseModel):
    """Model for Turso database query requests."""
    query: str = Field(..., description="SQL query to execute")
    database: Optional[str] = Field(None, description="Target database name")
    params: Optional[List[Any]] = Field(None, description="Query parameters")
    is_read_only: bool = Field(True, description="Whether query is read-only")

class TursoDatabaseInfo(BaseModel):
    """Model for Turso database information."""
    name: str = Field(..., description="Database name")
    status: str = Field(..., description="Database status")
    regions: List[str] = Field(default_factory=list, description="Database regions")
    created_at: Optional[str] = Field(None, description="Creation timestamp")

class TursoPerformanceReport(BaseModel):
    """Model for Turso performance analysis."""
    database: str = Field(..., description="Database analyzed")
    metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    recommendations: List[str] = Field(default_factory=list, description="Optimization recommendations")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class TursoSecurityAudit(BaseModel):
    """Model for Turso security audit results."""
    token_security: str = Field(..., description="Token security status")
    mcp_security: str = Field(..., description="MCP security status")
    access_control: str = Field(..., description="Access control status")
    recommendations: List[str] = Field(default_factory=list, description="Security recommendations")

# System prompt for Turso Specialist Agent
SYSTEM_PROMPT = """
You are a Turso Database Specialist Agent with deep expertise in:

**Core Expertise:**
- Turso Database (libSQL engine) operations and optimization
- MCP (Model Context Protocol) integration and setup
- Distributed database architecture and edge replication
- Security best practices and token management
- Performance optimization and troubleshooting

**Your Capabilities:**
- Database lifecycle management (create, configure, migrate, backup)
- MCP server setup and LLM integration
- Query optimization and schema design
- Security auditing and compliance
- Performance analysis and monitoring
- Troubleshooting complex distributed database issues

**Guidelines:**
- Always provide practical, actionable advice
- Include code examples when relevant
- Explain complex concepts clearly
- Prioritize security and best practices
- Use tools when you need to perform actual operations
- Validate configurations before suggesting changes

**Response Format:**
- Be comprehensive but concise
- Use emojis for visual clarity
- Structure information clearly
- Always suggest next steps
- Include relevant warnings for destructive operations
"""

# Initialize the Turso Specialist Agent - PydanticAI pattern
turso_specialist_agent = Agent(
    model=None,  # Will be set by get_llm_model()
    deps_type=TursoAgentDependencies,
    system_prompt=SYSTEM_PROMPT
)

@turso_specialist_agent.tool
async def list_turso_databases(
    ctx: RunContext[TursoAgentDependencies]
) -> List[TursoDatabaseInfo]:
    """
    List all Turso databases in the organization.
    
    Returns:
        List of database information with name, status, and regions
    """
    try:
        # Initialize Turso manager
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        turso_manager = TursoManager(settings)
        
        # Get databases
        databases = await turso_manager.list_databases()
        
        # Convert to structured format
        db_info_list = []
        for db in databases:
            db_info = TursoDatabaseInfo(
                name=db.get('name', 'Unknown'),
                status=db.get('status', 'Unknown'),
                regions=db.get('regions', []),
                created_at=db.get('created_at')
            )
            db_info_list.append(db_info)
        
        return db_info_list
        
    except Exception as e:
        return [TursoDatabaseInfo(
            name="Error",
            status=f"Failed to list databases: {str(e)}",
            regions=[]
        )]

@turso_specialist_agent.tool
async def create_turso_database(
    ctx: RunContext[TursoAgentDependencies],
    name: str,
    group: str = "default",
    regions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a new Turso database.
    
    Args:
        name: Database name
        group: Database group (default: "default")
        regions: List of regions for deployment
    
    Returns:
        Dictionary with creation results
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        turso_manager = TursoManager(settings)
        
        success = await turso_manager.create_database(name, group, regions)
        
        return {
            "success": success,
            "database_name": name,
            "group": group,
            "regions": regions or [],
            "message": f"Database '{name}' {'created successfully' if success else 'creation failed'}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "database_name": name
        }

@turso_specialist_agent.tool
async def execute_turso_query(
    ctx: RunContext[TursoAgentDependencies],
    query: str,
    database: Optional[str] = None,
    params: Optional[List[Any]] = None
) -> Dict[str, Any]:
    """
    Execute a query on Turso database.
    
    Args:
        query: SQL query to execute
        database: Target database (uses default if not specified)
        params: Query parameters
    
    Returns:
        Dictionary with query results
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        settings.default_database = database or ctx.deps.default_database
        
        turso_manager = TursoManager(settings)
        
        # Determine if query is read-only
        is_read_only = turso_manager._is_read_only_query(query)
        
        if is_read_only:
            result = await turso_manager.execute_read_only_query(query, database, params)
        else:
            result = await turso_manager.execute_query(query, database, params)
        
        return {
            "success": result.get('success', False),
            "result": result.get('result', ''),
            "error": result.get('error'),
            "query": query,
            "database": database or ctx.deps.default_database,
            "is_read_only": is_read_only
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "database": database or ctx.deps.default_database
        }

@turso_specialist_agent.tool
async def analyze_turso_performance(
    ctx: RunContext[TursoAgentDependencies],
    database: Optional[str] = None
) -> TursoPerformanceReport:
    """
    Analyze performance of Turso database.
    
    Args:
        database: Database to analyze (uses default if not specified)
    
    Returns:
        Performance analysis report
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        settings.default_database = database or ctx.deps.default_database
        
        turso_manager = TursoManager(settings)
        
        analysis = await turso_manager.analyze_performance(database)
        
        return TursoPerformanceReport(
            database=database or ctx.deps.default_database or "unknown",
            metrics=analysis.get('metrics', {}),
            recommendations=analysis.get('recommendations', [])
        )
        
    except Exception as e:
        return TursoPerformanceReport(
            database=database or ctx.deps.default_database or "unknown",
            metrics={"error": str(e)},
            recommendations=["Check database connectivity and permissions"]
        )

@turso_specialist_agent.tool
async def audit_turso_security(
    ctx: RunContext[TursoAgentDependencies]
) -> TursoSecurityAudit:
    """
    Perform security audit of Turso configuration.
    
    Returns:
        Security audit results
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        # Check token security
        token_status = await turso_manager._check_token_security()
        
        # Check MCP security
        mcp_security = await mcp_integrator.check_security()
        
        # Generate recommendations
        recommendations = []
        if "❌" in token_status:
            recommendations.append("Review token configuration and permissions")
        if "❌" in mcp_security:
            recommendations.append("Check MCP security configuration")
        
        return TursoSecurityAudit(
            token_security=token_status,
            mcp_security=mcp_security,
            access_control="✅ Configured" if "✅" in token_status else "❌ Issues detected",
            recommendations=recommendations
        )
        
    except Exception as e:
        return TursoSecurityAudit(
            token_security=f"❌ Error: {str(e)}",
            mcp_security="❌ Error during audit",
            access_control="❌ Error during audit",
            recommendations=["Check configuration and connectivity"]
        )

@turso_specialist_agent.tool
async def setup_mcp_integration(
    ctx: RunContext[TursoAgentDependencies]
) -> Dict[str, Any]:
    """
    Setup MCP Turso integration.
    
    Returns:
        MCP setup results
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        mcp_integrator = MCPTursoIntegrator(settings)
        
        setup_success = await mcp_integrator.setup_mcp_server()
        
        return {
            "success": setup_success,
            "message": "MCP Turso integration setup completed" if setup_success else "MCP setup failed",
            "next_steps": [
                "Configure LLM integration if setup was successful",
                "Test MCP connection",
                "Verify tools availability"
            ] if setup_success else [
                "Check Node.js installation",
                "Verify Turso API token",
                "Review error logs"
            ]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "MCP setup failed due to error"
        }

@turso_specialist_agent.tool
async def troubleshoot_turso_issue(
    ctx: RunContext[TursoAgentDependencies],
    issue_description: str
) -> Dict[str, Any]:
    """
    Troubleshoot Turso-related issues.
    
    Args:
        issue_description: Description of the issue to troubleshoot
    
    Returns:
        Troubleshooting results and recommendations
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        # Analyze issue type
        issue_lower = issue_description.lower()
        
        diagnostics = {
            "issue_type": "unknown",
            "diagnostics": [],
            "recommendations": []
        }
        
        if any(keyword in issue_lower for keyword in ['connection', 'auth', 'token']):
            diagnostics["issue_type"] = "authentication"
            diagnostics["diagnostics"].extend([
                "Check Turso API token validity",
                "Verify organization permissions",
                "Test CLI connectivity"
            ])
            diagnostics["recommendations"].extend([
                "Re-authenticate with `turso auth login`",
                "Verify token in environment variables",
                "Check organization access"
            ])
        
        elif any(keyword in issue_lower for keyword in ['performance', 'slow', 'timeout']):
            diagnostics["issue_type"] = "performance"
            diagnostics["diagnostics"].extend([
                "Analyze query execution plans",
                "Check database region selection",
                "Review connection pooling"
            ])
            diagnostics["recommendations"].extend([
                "Optimize query patterns",
                "Consider edge location selection",
                "Implement caching strategies"
            ])
        
        elif any(keyword in issue_lower for keyword in ['mcp', 'integration']):
            diagnostics["issue_type"] = "mcp_integration"
            diagnostics["diagnostics"].extend([
                "Check Node.js installation",
                "Verify MCP package installation",
                "Test MCP server connectivity"
            ])
            diagnostics["recommendations"].extend([
                "Install Node.js if missing",
                "Install MCP Turso package",
                "Configure LLM integration"
            ])
        
        return {
            "success": True,
            "issue_description": issue_description,
            "diagnostics": diagnostics,
            "next_steps": diagnostics["recommendations"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "issue_description": issue_description,
            "message": "Troubleshooting failed due to error"
        }

# Helper functions for agent creation
def create_turso_specialist_agent(
    turso_api_token: str,
    turso_organization: str,
    default_database: Optional[str] = None,
    session_id: Optional[str] = None,
    enable_mcp_integration: bool = True,
    debug_mode: bool = False
) -> Agent:
    """
    Create a Turso Specialist Agent with proper dependencies.
    
    Args:
        turso_api_token: Turso API token
        turso_organization: Turso organization name
        default_database: Default database to use
        session_id: Session identifier
        enable_mcp_integration: Whether to enable MCP integration
        debug_mode: Enable debug mode
    
    Returns:
        Configured Turso Specialist Agent
    """
    from ..config.turso_settings import TursoSettings
    from ..tools.turso_manager import TursoManager
    from ..tools.mcp_integrator import MCPTursoIntegrator
    
    # Configure settings
    settings = TursoSettings()
    settings.turso_api_token = turso_api_token
    settings.turso_organization = turso_organization
    settings.default_database = default_database
    
    # Create dependencies
    deps = TursoAgentDependencies(
        turso_api_token=turso_api_token,
        turso_organization=turso_organization,
        default_database=default_database,
        session_id=session_id,
        enable_mcp_integration=enable_mcp_integration,
        debug_mode=debug_mode
    )
    
    # Return configured agent
    return turso_specialist_agent

# Async chat function
async def chat_with_turso_specialist(
    message: str,
    deps: TursoAgentDependencies,
    use_test_model: bool = False
) -> str:
    """
    Chat with Turso Specialist Agent.
    
    Args:
        message: User message
        deps: Agent dependencies
        use_test_model: Whether to use TestModel for development
    
    Returns:
        Agent response
    """
    try:
        if use_test_model:
            test_model = TestModel()
            with turso_specialist_agent.override(model=test_model):
                result = await turso_specialist_agent.run(message, deps=deps)
        else:
            result = await turso_specialist_agent.run(message, deps=deps)
        
        return result.data
        
    except Exception as e:
        return f"❌ Error in Turso Specialist Agent: {str(e)}"

# Sync chat function
def chat_with_turso_specialist_sync(
    message: str,
    deps: TursoAgentDependencies,
    use_test_model: bool = False
) -> str:
    """
    Synchronous chat with Turso Specialist Agent.
    
    Args:
        message: User message
        deps: Agent dependencies
        use_test_model: Whether to use TestModel for development
    
    Returns:
        Agent response
    """
    try:
        if use_test_model:
            test_model = TestModel()
            with turso_specialist_agent.override(model=test_model):
                result = turso_specialist_agent.run_sync(message, deps=deps)
        else:
            result = turso_specialist_agent.run_sync(message, deps=deps)
        
        return result.data
        
    except Exception as e:
        return f"❌ Error in Turso Specialist Agent: {str(e)}" 