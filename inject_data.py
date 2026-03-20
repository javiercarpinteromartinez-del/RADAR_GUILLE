import json
import re

with open("c:\\Users\\javie\\RADAR_DTF\\real_leads.json", "r", encoding="utf-8") as f:
    leads = json.load(f)

json_str = json.dumps(leads, ensure_ascii=False, indent=4)

with open("c:\\Users\\javie\\RADAR_DTF\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the array
pattern = r'(?s)const D = \[.*?\];'
replacement = f"let D = JSON.parse(localStorage.getItem('dtf_leads'));\nif (!D || D.length === 0) {{\n    D = {json_str};\n    localStorage.setItem('dtf_leads', JSON.stringify(D));\n}}"
new_html = re.sub(pattern, replacement, html, count=1)

# Add logic for dynamic adding and updating state
add_prospect_function = """
        function addLead() {
            const name = prompt("Nombre de la empresa:");
            if(!name) return;
            const sector = prompt("Sector (Serigrafía, Copistería, Deportes, Ropa Laboral):", "Serigrafía");
            const city = prompt("Ciudad:", "Madrid");
            const vol = parseInt(prompt("Volumen estimado m/mes:", "50")) || 50;
            const newLead = {
                id: Date.now(),
                name: name,
                city: city,
                sector: sector,
                equip: "Desconocido",
                vol: vol,
                score: 85,
                opp: "Prospecto añadido manualmente",
                status: "No contactado"
            };
            D.push(newLead);
            localStorage.setItem('dtf_leads', JSON.stringify(D));
            renderTable();
        }
        
        function updateLeadStatus(id, newStatus) {
            const lead = D.find(d => d.id == id);
            if(lead) {
                lead.status = newStatus;
                localStorage.setItem('dtf_leads', JSON.stringify(D));
                renderTable();
            }
        }
"""

new_html = new_html.replace('function renderTable() {', add_prospect_function + '\n        function renderTable() {')
new_html = new_html.replace('<button class="btn btn-primary">+ Nuevo Contacto</button>', '<button class="btn btn-primary" onclick="addLead()">+ Nuevo Contacto</button>')

# Update table rendering HTML logic via regex for robustness
new_html = new_html.replace('<th>DTF Score</th>\\n                            <th>Acción</th>', '<th>DTF Score</th>\\n                            <th>Estado CRM</th>\\n                            <th>Acción</th>')

new_html = new_html.replace('<th>DTF Score</th>\n                            <th>Acción</th>', '<th>DTF Score</th>\n                            <th>Estado CRM</th>\n                            <th>Acción</th>')

row_replacement = '<td>\\n                        <span class="badge badge-score ${lead.score >= 90 ? \\\'high\\\' : \\\'\\\'}">${lead.score}</span>\\n                    </td>\\n                    <td><span class="badge badge-sector" style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:#fff">${lead.status || \\\'No contactado\\\'}</span></td>'

new_html = new_html.replace('<td>\n                        <span class="badge badge-score ${lead.score >= 90 ? \'high\' : \'\'}">${lead.score}</span>\n                    </td>', '<td>\n                        <span class="badge badge-score ${lead.score >= 90 ? \'high\' : \'\'}">${lead.score}</span>\n                    </td>\n                    <td><span class="badge" style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:#FFF">${lead.status || \'No contactado\'}</span></td>')

new_html = new_html.replace('onclick="closeModal(); alert(\\\'Marcado como muestra enviada.\\\')"', 'onclick="updateLeadStatus(document.getElementById(\\\'modal\\\').getAttribute(\\\'data-id\\\'), \\\'Muestra enviada\\\'); closeModal();"')

new_html = new_html.replace("modal.style.display = 'block';", "modal.setAttribute('data-id', id);\n            modal.style.display = 'block';")

with open("c:\\Users\\javie\\RADAR_DTF\\index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Injected real leads and LocalStorage CRM logic successfully!")
