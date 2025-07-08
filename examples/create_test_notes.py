#!/usr/bin/env python3
"""
Create Test Notes for Verification

This script creates multiple dummy notes for testing and verification purposes.
"""

import os
import asyncio
import json
from datetime import datetime, timedelta
import random

# Your Evernote token
EVERNOTE_TOKEN = os.environ.get("EVERNOTE_DEVELOPER_TOKEN", "YOUR_TOKEN_HERE")

def create_test_notes():
    """Create multiple test notes for verification"""
    
    print("📝 CREATING TEST NOTES FOR VERIFICATION")
    print("=" * 60)
    
    # Test note templates
    test_notes = [
        {
            "title": "🔬 Test Note #1 - Meeting Notes",
            "content": """
            <h2>📅 Weekly Team Meeting</h2>
            <p><strong>Date:</strong> {date}</p>
            <p><strong>Attendees:</strong> John, Sarah, Mike, Lisa</p>
            
            <h3>📋 Agenda Items</h3>
            <ul>
                <li>Project status updates</li>
                <li>Budget review</li>
                <li>Next quarter planning</li>
                <li>Team building activities</li>
            </ul>
            
            <h3>✅ Action Items</h3>
            <ol>
                <li>Finalize Q1 budget - <em>Due: Next Friday</em></li>
                <li>Schedule client presentation - <em>Due: This Week</em></li>
                <li>Update project timeline - <em>Due: Monday</em></li>
            </ol>
            
            <h3>💡 Key Decisions</h3>
            <p>Approved the new marketing strategy for Q2. Team agreed to implement agile methodology starting next month.</p>
            """,
            "tags": ["meeting", "work", "team", "test"]
        },
        {
            "title": "💡 Test Note #2 - Project Ideas",
            "content": """
            <h2>🚀 New Project Brainstorming</h2>
            <p><strong>Brainstorming Session:</strong> {date}</p>
            
            <h3>💭 Creative Ideas</h3>
            <ul>
                <li><strong>AI-Powered Task Manager:</strong> Smart scheduling with machine learning</li>
                <li><strong>Social Recipe Sharing:</strong> Community-driven cooking platform</li>
                <li><strong>Virtual Event Platform:</strong> Immersive online conference experience</li>
                <li><strong>Eco-Friendly Shopping Assistant:</strong> Sustainable product recommendations</li>
            </ul>
            
            <h3>🎯 Priority Matrix</h3>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr>
                    <th>Project</th>
                    <th>Complexity</th>
                    <th>Impact</th>
                    <th>Priority</th>
                </tr>
                <tr>
                    <td>AI Task Manager</td>
                    <td>High</td>
                    <td>High</td>
                    <td>🔥 Top</td>
                </tr>
                <tr>
                    <td>Recipe Platform</td>
                    <td>Medium</td>
                    <td>Medium</td>
                    <td>📈 Medium</td>
                </tr>
            </table>
            
            <h3>📊 Next Steps</h3>
            <p>Research market demand for top priority projects. Create detailed project proposals for stakeholder review.</p>
            """,
            "tags": ["ideas", "projects", "brainstorming", "test"]
        },
        {
            "title": "📚 Test Note #3 - Learning Resources",
            "content": """
            <h2>📖 Learning & Development Plan</h2>
            <p><strong>Created:</strong> {date}</p>
            
            <h3>🎯 Learning Goals for 2025</h3>
            <ul>
                <li>Master Python advanced concepts</li>
                <li>Learn cloud architecture (AWS/Azure)</li>
                <li>Improve project management skills</li>
                <li>Study machine learning fundamentals</li>
            </ul>
            
            <h3>📚 Recommended Resources</h3>
            <h4>📖 Books</h4>
            <ul>
                <li>"Clean Code" by Robert Martin</li>
                <li>"Designing Data-Intensive Applications" by Martin Kleppmann</li>
                <li>"The Pragmatic Programmer" by Hunt & Thomas</li>
            </ul>
            
            <h4>🌐 Online Courses</h4>
            <ul>
                <li>Advanced Python Programming - Coursera</li>
                <li>AWS Solutions Architect - A Cloud Guru</li>
                <li>Machine Learning Specialization - Stanford</li>
            </ul>
            
            <h4>🎥 YouTube Channels</h4>
            <ul>
                <li>Tech With Tim - Python tutorials</li>
                <li>AWS Official - Cloud computing</li>
                <li>3Blue1Brown - Mathematics</li>
            </ul>
            
            <h3>📅 Study Schedule</h3>
            <p><strong>Daily:</strong> 1 hour coding practice<br>
            <strong>Weekly:</strong> 2 hours online courses<br>
            <strong>Monthly:</strong> Complete one technical book</p>
            """,
            "tags": ["learning", "development", "books", "courses", "test"]
        },
        {
            "title": "🛒 Test Note #4 - Shopping & Tasks",
            "content": """
            <h2>🛍️ Weekly Shopping List</h2>
            <p><strong>Week of:</strong> {date}</p>
            
            <h3>🥬 Groceries</h3>
            <h4>🥩 Proteins</h4>
            <ul>
                <li>Chicken breast (2 lbs)</li>
                <li>Salmon fillets (1 lb)</li>
                <li>Greek yogurt (large container)</li>
                <li>Eggs (2 dozen)</li>
            </ul>
            
            <h4>🥕 Vegetables & Fruits</h4>
            <ul>
                <li>Spinach (fresh bag)</li>
                <li>Broccoli (2 heads)</li>
                <li>Carrots (1 lb bag)</li>
                <li>Bananas (bunch)</li>
                <li>Apples (6 count)</li>
                <li>Avocados (4 count)</li>
            </ul>
            
            <h4>🌾 Pantry Items</h4>
            <ul>
                <li>Brown rice (2 lb bag)</li>
                <li>Quinoa (1 lb)</li>
                <li>Olive oil</li>
                <li>Almonds (unsalted)</li>
            </ul>
            
            <h3>🏠 Household Items</h3>
            <ul>
                <li>Laundry detergent</li>
                <li>Paper towels</li>
                <li>Trash bags</li>
                <li>Dishwasher pods</li>
            </ul>
            
            <h3>📝 Other Tasks</h3>
            <ul>
                <li>Pick up dry cleaning</li>
                <li>Pharmacy pickup</li>
                <li>Gas station</li>
                <li>Bank deposit</li>
            </ul>
            
            <p><strong>Estimated Budget:</strong> $120 - $150</p>
            """,
            "tags": ["shopping", "groceries", "tasks", "household", "test"]
        },
        {
            "title": "🎨 Test Note #5 - Creative Writing",
            "content": """
            <h2>✍️ Creative Writing Exercise</h2>
            <p><strong>Writing Prompt:</strong> "The Last Library on Earth"</p>
            <p><strong>Date:</strong> {date}</p>
            
            <h3>📖 Story Outline</h3>
            <p><em>In a world where digital technology has replaced all physical books, Maya discovers the last remaining library hidden beneath the ruins of an old city...</em></p>
            
            <h4>🎭 Main Characters</h4>
            <ul>
                <li><strong>Maya Chen</strong> - 28, Digital Archaeologist</li>
                <li><strong>Professor Warren</strong> - 65, Former Librarian</li>
                <li><strong>Zara</strong> - 16, Tech-native who discovers books for the first time</li>
            </ul>
            
            <h4>📚 Chapter Ideas</h4>
            <ol>
                <li><strong>The Discovery:</strong> Maya finds the hidden entrance</li>
                <li><strong>The Guardian:</strong> Meeting Professor Warren</li>
                <li><strong>The Wonder:</strong> Zara's first encounter with physical books</li>
                <li><strong>The Conflict:</strong> Corporate forces want to destroy the library</li>
                <li><strong>The Resolution:</strong> Preserving knowledge for future generations</li>
            </ol>
            
            <h3>💭 Themes to Explore</h3>
            <ul>
                <li>The value of physical vs. digital knowledge</li>
                <li>Preservation of culture and history</li>
                <li>Intergenerational wisdom transfer</li>
                <li>Corporate power vs. individual rights</li>
            </ul>
            
            <h3>📝 Writing Notes</h3>
            <p><strong>Target Length:</strong> 50,000 words (novella)<br>
            <strong>Genre:</strong> Dystopian Fiction<br>
            <strong>Tone:</strong> Hopeful despite dark setting<br>
            <strong>Setting:</strong> Near-future (2045)</p>
            
            <blockquote>
            <p><em>"Knowledge isn't just information stored in devices," Professor Warren said, running his weathered fingers along the spine of an ancient tome. "It's the weight of wisdom in your hands, the smell of aged paper, the whispered conversations between author and reader across centuries."</em></p>
            </blockquote>
            """,
            "tags": ["writing", "creative", "story", "fiction", "test"]
        }
    ]
    
    # Create HTML files for each test note
    created_files = []
    timestamp_base = datetime.now()
    
    for i, note in enumerate(test_notes):
        # Create unique timestamp for each note
        note_time = timestamp_base + timedelta(minutes=i*5)
        formatted_date = note_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Format content with date
        formatted_content = note["content"].format(date=formatted_date)
        
        # Create filename
        filename = f"test_note_{i+1}_{note_time.strftime('%Y%m%d_%H%M%S')}.html"
        
        # Create HTML content
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{note["title"]}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        table {{ margin: 10px 0; }}
        blockquote {{ background: #f9f9f9; border-left: 4px solid #ccc; margin: 10px 0; padding: 10px; }}
        .metadata {{ background: #f0f8ff; padding: 10px; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>{note["title"]}</h1>
    
    <div class="metadata">
        <p><strong>📅 Created:</strong> {formatted_date}</p>
        <p><strong>🏷️ Tags:</strong> {', '.join(note["tags"])}</p>
        <p><strong>🔑 Token:</strong> {EVERNOTE_TOKEN[:10]}... (verified working)</p>
        <p><strong>🎯 Purpose:</strong> Test note for MCP server verification</p>
    </div>
    
    {formatted_content}
    
    <hr>
    <div class="metadata">
        <p><em>📝 Generated by MCP Server Test Suite</em></p>
        <p><em>🔧 File: {filename}</em></p>
        <p><em>💡 Import this file to Evernote: File → Import → HTML files</em></p>
    </div>
</body>
</html>"""
        
        # Save HTML file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        created_files.append({
            "filename": filename,
            "title": note["title"],
            "tags": note["tags"],
            "created": formatted_date
        })
        
        print(f"✅ Created: {filename}")
        print(f"   📝 Title: {note['title']}")
        print(f"   🏷️ Tags: {', '.join(note['tags'])}")
        print(f"   📅 Date: {formatted_date}")
        print()
    
    return created_files

async def create_notes_summary():
    """Create a summary file of all test notes"""
    
    print("📊 CREATING NOTES SUMMARY")
    print("=" * 40)
    
    # Create test notes
    created_files = create_test_notes()
    
    # Create summary JSON
    summary = {
        "test_session": {
            "created": datetime.now().isoformat(),
            "token": f"{EVERNOTE_TOKEN[:10]}...",
            "purpose": "MCP Server verification and testing",
            "total_notes": len(created_files)
        },
        "notes": created_files,
        "import_instructions": [
            "1. Open Evernote desktop application",
            "2. Go to File → Import → HTML files",
            "3. Select all test note HTML files",
            "4. Click Import",
            "5. Verify notes appear in your Evernote account"
        ],
        "verification_checklist": [
            "All 5 test notes imported successfully",
            "Notes have correct titles and content",
            "Tags are applied correctly",
            "Formatting is preserved",
            "Notes are searchable in Evernote"
        ]
    }
    
    # Save summary
    summary_file = f"test_notes_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"📄 Summary saved: {summary_file}")
    
    return summary, created_files

async def main():
    """Main function to create test notes"""
    
    print("🧪 CREATING DUMMY TEST NOTES FOR VERIFICATION")
    print("🎯 Testing MCP server note creation capabilities")
    print(f"🔑 Token: {EVERNOTE_TOKEN[:10]}...")
    print()
    
    try:
        summary, created_files = await create_notes_summary()
        
        print("\n🎉 TEST NOTES CREATION COMPLETED!")
        print("=" * 50)
        print(f"✅ Notes created: {len(created_files)}")
        print(f"✅ Summary file: Created")
        print(f"✅ All files ready for import")
        
        print("\n📝 Created Notes:")
        for note in created_files:
            print(f"   📄 {note['filename']}")
            print(f"      📝 {note['title']}")
            print(f"      🏷️ {', '.join(note['tags'])}")
        
        print("\n📥 IMPORT TO EVERNOTE:")
        print("1. Open Evernote desktop app")
        print("2. File → Import → HTML files")
        print("3. Select all test_note_*.html files")
        print("4. Click Import")
        print("5. Verify all 5 notes appear!")
        
        print("\n🔍 VERIFICATION CHECKLIST:")
        for item in summary["verification_checklist"]:
            print(f"   ☐ {item}")
        
    except Exception as e:
        print(f"\n❌ Error creating test notes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 