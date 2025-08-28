# YouAreCapitalist Documentation

## 📚 Documentation Guidelines

### Directory Structure
```
.claude/doc/
├── api/              # API documentation and references
├── guides/           # User guides and tutorials  
├── architecture/     # System architecture and design docs
├── references/       # Technical references and specifications
└── templates/        # Documentation templates
```

### Documentation Standards

#### File Naming
- Use lowercase with hyphens: `game-mechanics.md`, `api-reference.md`
- Include version in filename when applicable: `api-v1.0.md`
- Date format for changelogs: `changelog-2025-01.md`

#### Document Structure
Every document should include:
1. **Title** - Clear, descriptive heading
2. **Metadata** - Date, version, author (if applicable)
3. **Table of Contents** - For documents > 3 sections
4. **Overview** - Brief description of content
5. **Main Content** - Organized with clear headings
6. **References** - Links to related documentation

#### Markdown Conventions
- Use ATX-style headers (`#`, `##`, `###`)
- Code blocks with language specification
- Tables for structured data
- Link to other docs using relative paths

### Documentation Types

#### API Documentation (`/api`)
- Endpoint specifications
- Request/response formats
- Authentication details
- Error codes and handling

#### Guides (`/guides`)
- Getting started guides
- Feature tutorials
- Best practices
- Troubleshooting guides

#### Architecture (`/architecture`)
- System design documents
- Component diagrams
- Data flow diagrams
- Technical decisions

#### References (`/references`)
- Configuration options
- Environment variables
- Technical specifications
- Glossary of terms

### Documentation Workflow

1. **Planning**
   - Identify documentation needs
   - Determine target audience
   - Choose appropriate template

2. **Creation**
   - Use templates from `/templates` directory
   - Follow naming conventions
   - Include all required sections

3. **Review**
   - Verify technical accuracy
   - Check for completeness
   - Ensure clarity and readability

4. **Maintenance**
   - Update version numbers
   - Add changelog entries
   - Archive deprecated documentation

### Templates Location
Documentation templates are available in `.claude/doc/templates/` directory.

### Cross-References
- Use relative paths: `[See API Guide](../api/api-guide.md)`
- Maintain link integrity when moving files
- Update references when restructuring

### Version Control
- Track all documentation changes
- Use meaningful commit messages
- Tag major documentation releases
- Archive outdated versions appropriately

## Quick Start
To create new documentation:
1. Choose the appropriate subdirectory
2. Use relevant template from `/templates`
3. Follow the naming conventions
4. Include required metadata
5. Commit with descriptive message

---
*Last Updated: 2025-01-28*  
*Documentation Version: 1.0*