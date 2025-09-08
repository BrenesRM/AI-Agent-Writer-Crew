        "beta_reader": "Provides reader perspective feedback",
        "lorekeeper": "Manages world-building and lore consistency",
        "proofreader": "Corrects grammar and language errors",
        "innovation_scout": "Identifies creative opportunities",
        "visualizer": "Creates visual narrative descriptions",
        "pacing_specialist": "Optimizes story pacing and rhythm"
    }
    return descriptions.get(agent_name, "AI writing assistant")

def get_agent_icon(agent_name: str) -> str:
    """Get icon for agent"""
    icons = {
        "researcher": "🔍",
        "character_developer": "👥",
        "plot_weaver": "🕸️",
        "style_editor": "✍️",
        "continuity_auditor": "📋",
        "beta_reader": "📖",
        "lorekeeper": "📚",
        "proofreader": "🔤",
        "innovation_scout": "💡",
        "visualizer": "🎨",
        "pacing_specialist": "⏱️"
    }
    return icons.get(agent_name, "🤖")

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
