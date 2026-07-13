from supabase import create_client

SUPABASE_URL = "https://wanwjfizrjbubhpewwpf.supabase.co"

SUPABASE_KEY = "sb_publishable_swLiF7DLGVOnhxsvZUV9cQ_ViUwPYNx"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)