-- Inicialização do banco de dados
-- Extensões
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Índices adicionais para performance
CREATE INDEX IF NOT EXISTS idx_questions_disciplina ON questions(disciplina);
CREATE INDEX IF NOT EXISTS idx_questions_topico ON questions(topico);
CREATE INDEX IF NOT EXISTS idx_questions_dificuldade ON questions(dificuldade);
CREATE INDEX IF NOT EXISTS idx_questions_qa_status ON questions(qa_status);

CREATE INDEX IF NOT EXISTS idx_user_answers_user_id ON user_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_question_id ON user_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_answered_at ON user_answers(answered_at);

CREATE INDEX IF NOT EXISTS idx_simulado_results_user_id ON simulado_results(user_id);
CREATE INDEX IF NOT EXISTS idx_simulado_results_simulado_id ON simulado_results(simulado_id);
