"""
Módulo de templates para diferentes tipos de descrições de e-commerce
"""

TEMPLATES = {
    "shopee_mercado_livre": {
        "name": "Shopee/Mercado Livre",
        "description": "Otimizado para marketplaces brasileiros",
        "instructions": """
        - Formato compacto e direto
        - Use emojis atraentes (⭐🔥💎✨)
        - Destaque frete grátis e promoções
        - Incluir medidas em cm e kg
        - Chamar atenção para avaliações
        - Formato: Título + Bullet Points + Especificações
        - Incluir: "Envio imediato" e "Compra segura"
        """
    },
    "amazon_style": {
        "name": "Estilo Amazon",
        "description": "Formato profissional estilo Amazon",
        "instructions": """
        - Estrutura formal e detalhada
        - Título técnico e descritivo
        - Seção "Características Principais"
        - Seção "Especificações Técnicas" em tabela
        - Seção "O que está incluído na caixa"
        - Foco em benefícios e diferenciais
        - Incluir FAQ breve
        - Tom profissional e confiável
        """
    },
    "redes_sociais": {
        "name": "Redes Sociais",
        "description": "Descrição para Instagram/Facebook",
        "instructions": """
        - Tom descontraído e conversacional
        - Use emojis criativos e relevantes
        - Incluir perguntas para engajamento
        - Formato: Capa + Descrição + Hashtags
        - Destaque ofertas exclusivas
        - Incluir call-to-action claro
        - Usar linhas em branco para separação
        - Hashtags estratégicas no final
        """
    },
    "seo_otimizado": {
        "name": "SEO Otimizado",
        "description": "Foco máximo em SEO",
        "instructions": """
        - Palavra-chave no início do título
        - Repetir palavra-chave naturalmente (2-3%)
        - Estrutura H1, H2, H3 implícita
        - Texto com 300+ palavras
        - Meta-descrição otimizada
        - URLs amigáveis sugeridas
        - Schema markup sugerido
        - Foco em autoridade e confiança
        """
    },
    "copy_persuasivo": {
        "name": "Copy Persuasivo",
        "description": "Foco em vendas e conversão",
        "instructions": """
        - Copywriting de alta conversão
        - Gatilhos mentais (urgência, escassez)
        - História emocional do produto
        - Testemunhos e prova social
        - Garantia estendida
        - Oferta irrecusável
        - Call-to-action forte
        - Remoção de objeções
        """
    },
    "luxo_premium": {
        "name": "Luxo/Premium",
        "description": "Produtos de alto valor",
        "instructions": """
        - Tom sofisticado e exclusivo
        - Destaque materiais premium
        - História da marca
        - Artesanato/processo especial
        - Certificações e selos
        - Embalagem de luxo
        - Experiência do cliente
        - Exclusividade e limite
        """
    }
}

def get_template_instructions(template_key):
    """Retorna as instruções de um template específico"""
    return TEMPLATES.get(template_key, {}).get("instructions", "")

def get_all_templates():
    """Retorna todos os templates disponíveis"""
    return TEMPLATES

def get_template_name(template_key):
    """Retorna o nome amigável de um template"""
    return TEMPLATES.get(template_key, {}).get("name", "Padrão")