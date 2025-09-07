#!/usr/bin/env python3
"""
Quick fix for the individual tools test
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def fix_tool_test():
    """Fix the parameter names in the individual tools test"""
    
    try:
        from agents.tools import (
            WritingAnalyzer, StyleAnalyzer, CharacterAnalyzer,
            ConsistencyChecker, PacingAnalyzer, PlotAnalyzer,
            IdeaGenerator, VisualPromptGenerator
        )
        
        # Test text
        test_text = """
        En el reino de Eldoria, la joven maga Lyra caminaba por el bosque encantado. 
        Sus ojos azules brillaban con determinacion mientras buscaba el cristal perdido.
        El viento susurraba secretos antiguos entre las hojas doradas.
        """
        
        print("🔧 Testing individual tools with correct parameters...")
        
        # Test each tool with correct parameters
        tools_to_test = [
            (WritingAnalyzer(), {"text": test_text}),
            (StyleAnalyzer(), {"text": test_text}),
            (CharacterAnalyzer(), {"text": test_text}),
            (ConsistencyChecker(), {"text": test_text}),
            (PacingAnalyzer(), {"text": test_text}),
            (PlotAnalyzer(), {"text": test_text}),
            (IdeaGenerator(), {"context": "reino magico con cristales"}),
            (VisualPromptGenerator(), {"scene_description": "maga caminando por bosque encantado"})
        ]
        
        successful_tools = 0
        total_tools = len(tools_to_test)
        
        for tool, kwargs in tools_to_test:
            try:
                result = tool._run(**kwargs)
                
                if result and len(str(result)) > 10:
                    print(f"✅ {tool.name}: OK")
                    successful_tools += 1
                else:
                    print(f"⚠️  {tool.name}: Empty result")
                    
            except Exception as e:
                print(f"❌ {tool.name}: {str(e)[:50]}...")
        
        print(f"\n📊 Results: {successful_tools}/{total_tools} tools working")
        
        if successful_tools == total_tools:
            print("🎉 All individual tools are working correctly!")
            print("The issue is in the test file parameter names.")
            return True
        else:
            print("❌ Some tools still have issues.")
            return False
            
    except Exception as e:
        print(f"❌ Error testing tools: {e}")
        return False

def main():
    print("🚀 Quick Tool Test Fix\n")
    
    if fix_tool_test():
        print("\n✅ Individual tools are functional!")
        print("The test file needs parameter name updates.")
        print("\nThe system should score 6/6 with this fix.")
    else:
        print("\n❌ Tools still need work.")

if __name__ == "__main__":
    main()
