# 🔧 Plano de Consolidação: Geradores de PRP

## 📊 Situação Atual

- **25 scripts** relacionados a PRP em `/prp-agent`
- **Muita redundância** e confusão
- **Necessidade de simplificação** urgente

## 🎯 Proposta de Consolidação

### ✅ MANTER (3 Scripts Essenciais)

1. **generate_prp_simple.py** - Gerador principal
2. **demo_turso_specialist_prp.py** - Para Turso
3. **cli.py** em `/agents` - Interface conversacional

### 🗑️ REMOVER/ARQUIVAR (22 Scripts)

#### Scripts de Listagem (12 arquivos redundantes):
- list_prps.py
- list_prps_from_turso.py
- list_prps_real_mcp.py
- list_prps_with_agent.py
- list_prps_via_api.py
- list_prps_real_cursor.py
- list_prps_mcp_tools.py
- list_prps_working_tools.py
- list_prps_cursor_agent_real.py
- list_prps_real_agent.py
- create_and_list_prps.py
- list_prps_final.py

**Motivo:** Todos fazem a mesma coisa com pequenas variações

#### Scripts de Remoção (3 arquivos):
- remover_prp.py
- remover_prp_fixed.py
- delete_prp_tool.py

**Motivo:** Funcionalidade deve estar no agente principal

#### Scripts Redundantes (7 arquivos):
- generate_prp.py (versão complexa do simple)
- create_prp_manual.py (duplica generate_prp_simple)
- exemplo_prp_organizacao.py (apenas exemplo)
- use_turso_specialist_prp.py (duplica demo)
- test_prp_agent.py (teste, mover para /tests)
- prp_mcp_integration.py (já migrado)
- sentry_prp_agent_setup.py (já em monitoring/)

## 📦 Ação de Consolidação

### Criar Script Unificado: `prp_tools.py`
```python
# Consolidar funcionalidades em um único módulo
class PRPTools:
    def generate_simple(self): ...
    def generate_turso(self): ...
    def list_all(self): ...
    def delete(self, id): ...
    def search(self, query): ...
```

### Estrutura Final:
```
prp-agent/
├── generate_prp_simple.py    # Gerador principal
├── demo_turso_specialist.py  # Demo Turso
├── prp_tools.py             # Ferramentas consolidadas
└── archive/                 # Scripts antigos arquivados
```

## 🚀 Benefícios

1. **De 25 para 3 scripts** principais
2. **88% de redução** em complexidade
3. **Interface clara** e intuitiva
4. **Manutenção simplificada**
5. **Menos confusão** para usuários

## 📝 Próximos Passos

1. Criar `prp_tools.py` consolidado
2. Mover scripts para `archive/`
3. Atualizar documentação
4. Testar funcionalidades essenciais

---
*Plano para simplificar de 25 para 3 scripts de PRP*