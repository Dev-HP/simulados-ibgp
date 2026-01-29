import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function AdaptiveLearning() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);
  const [studyPlan, setStudyPlan] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [activeTab, setActiveTab] = useState('analysis');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };

      // Carregar análise
      const analysisRes = await axios.get(`${API_URL}/api/adaptive/analyze`, config);
      setAnalysis(analysisRes.data);

      // Carregar plano de estudos
      const planRes = await axios.get(`${API_URL}/api/adaptive/study-plan?days=7`, config);
      setStudyPlan(planRes.data);

      // Carregar previsão
      const predictionRes = await axios.get(`${API_URL}/api/adaptive/predict-performance`, config);
      setPrediction(predictionRes.data);

      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      if (error.response?.status === 401) {
        navigate('/login');
      }
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Analisando seu desempenho...</p>
        </div>
      </div>
    );
  }

  if (analysis?.status === 'insufficient_data') {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={() => navigate('/dashboard')}
            className="mb-6 text-indigo-600 hover:text-indigo-800 flex items-center"
          >
            ← Voltar ao Dashboard
          </button>

          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="text-6xl mb-4">📊</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Dados Insuficientes
            </h2>
            <p className="text-gray-600 mb-6">
              {analysis.message}
            </p>
            <button
              onClick={() => navigate('/simulados')}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700"
            >
              Fazer Simulado Agora
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="mb-4 text-indigo-600 hover:text-indigo-800 flex items-center"
          >
            ← Voltar ao Dashboard
          </button>
          <h1 className="text-3xl font-bold text-gray-800">
            🧠 Aprendizado Adaptativo
          </h1>
          <p className="text-gray-600 mt-2">
            Análise personalizada do seu desempenho e recomendações inteligentes
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-lg mb-6">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('analysis')}
              className={`flex-1 py-4 px-6 text-center font-medium ${
                activeTab === 'analysis'
                  ? 'border-b-2 border-indigo-600 text-indigo-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              📊 Análise
            </button>
            <button
              onClick={() => setActiveTab('plan')}
              className={`flex-1 py-4 px-6 text-center font-medium ${
                activeTab === 'plan'
                  ? 'border-b-2 border-indigo-600 text-indigo-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              📅 Plano de Estudos
            </button>
            <button
              onClick={() => setActiveTab('prediction')}
              className={`flex-1 py-4 px-6 text-center font-medium ${
                activeTab === 'prediction'
                  ? 'border-b-2 border-indigo-600 text-indigo-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              🎯 Previsão
            </button>
          </div>
        </div>

        {/* Content */}
        {activeTab === 'analysis' && analysis && (
          <div className="space-y-6">
            {/* Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <div className="text-4xl font-bold text-indigo-600">
                  {analysis.overall_accuracy}%
                </div>
                <div className="text-gray-600 mt-2">Acurácia Geral</div>
              </div>
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <div className="text-4xl font-bold text-green-600">
                  {analysis.total_questions_answered}
                </div>
                <div className="text-gray-600 mt-2">Questões Respondidas</div>
              </div>
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <div className="text-4xl font-bold text-purple-600">
                  {analysis.topics_analyzed}
                </div>
                <div className="text-gray-600 mt-2">Tópicos Analisados</div>
              </div>
            </div>

            {/* Learning Pattern */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                📈 Padrão de Aprendizado
              </h3>
              <div className="flex items-center space-x-4">
                <div className="text-4xl">
                  {analysis.learning_pattern === 'improving' && '📈'}
                  {analysis.learning_pattern === 'declining' && '📉'}
                  {analysis.learning_pattern === 'consistent' && '➡️'}
                  {analysis.learning_pattern === 'volatile' && '📊'}
                </div>
                <div>
                  <div className="font-semibold text-gray-800">
                    {analysis.learning_pattern === 'improving' && 'Melhorando'}
                    {analysis.learning_pattern === 'declining' && 'Piorando'}
                    {analysis.learning_pattern === 'consistent' && 'Consistente'}
                    {analysis.learning_pattern === 'volatile' && 'Variável'}
                  </div>
                  <div className="text-gray-600 text-sm">
                    Dificuldade recomendada: {analysis.recommended_difficulty}
                  </div>
                </div>
              </div>
            </div>

            {/* Weak Topics */}
            {analysis.weak_topics && analysis.weak_topics.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-xl font-bold text-red-600 mb-4">
                  ⚠️ Tópicos que Precisam de Atenção
                </h3>
                <div className="space-y-3">
                  {analysis.weak_topics.map((topic, index) => (
                    <div key={index} className="border-l-4 border-red-500 pl-4 py-2">
                      <div className="font-semibold text-gray-800">
                        {topic.disciplina} - {topic.topico}
                      </div>
                      <div className="flex items-center justify-between mt-1">
                        <span className="text-sm text-gray-600">
                          {topic.total_questions} questões respondidas
                        </span>
                        <span className="text-red-600 font-bold">
                          {topic.accuracy.toFixed(1)}% acerto
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Strong Topics */}
            {analysis.strong_topics && analysis.strong_topics.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-xl font-bold text-green-600 mb-4">
                  ✅ Seus Pontos Fortes
                </h3>
                <div className="space-y-3">
                  {analysis.strong_topics.map((topic, index) => (
                    <div key={index} className="border-l-4 border-green-500 pl-4 py-2">
                      <div className="font-semibold text-gray-800">
                        {topic.disciplina} - {topic.topico}
                      </div>
                      <div className="flex items-center justify-between mt-1">
                        <span className="text-sm text-gray-600">
                          {topic.total_questions} questões respondidas
                        </span>
                        <span className="text-green-600 font-bold">
                          {topic.accuracy.toFixed(1)}% acerto
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'plan' && studyPlan && studyPlan.status === 'success' && (
          <div className="space-y-6">
            {/* Plan Overview */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                📅 Plano de 7 Dias
              </h3>
              <p className="text-gray-600 mb-4">
                {studyPlan.estimated_improvement}
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-indigo-50 p-4 rounded-lg">
                  <div className="text-sm text-gray-600">Acurácia Atual</div>
                  <div className="text-2xl font-bold text-indigo-600">
                    {studyPlan.overall_accuracy.toFixed(1)}%
                  </div>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="text-sm text-gray-600">Padrão</div>
                  <div className="text-2xl font-bold text-purple-600">
                    {studyPlan.learning_pattern}
                  </div>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="text-sm text-gray-600">Duração</div>
                  <div className="text-2xl font-bold text-green-600">
                    {studyPlan.plan_duration_days} dias
                  </div>
                </div>
              </div>
            </div>

            {/* Daily Plan */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                📋 Plano Diário
              </h3>
              <div className="space-y-4">
                {studyPlan.daily_plan.map((day) => (
                  <div key={day.day} className="border rounded-lg p-4 hover:shadow-md transition">
                    <div className="flex items-center justify-between mb-2">
                      <div className="font-bold text-gray-800">
                        Dia {day.day}
                      </div>
                      <div className="text-sm text-gray-600">
                        {day.recommended_questions} questões
                      </div>
                    </div>
                    {day.focus === 'weak_topic' ? (
                      <div>
                        <div className="text-sm font-semibold text-red-600 mb-1">
                          🎯 Foco: {day.disciplina} - {day.topico}
                        </div>
                        <div className="text-sm text-gray-600 mb-2">
                          Acurácia atual: {day.current_accuracy.toFixed(1)}% → Meta: {day.target_accuracy}%
                        </div>
                        <div className="text-sm text-gray-600 italic">
                          💡 {day.tip}
                        </div>
                      </div>
                    ) : (
                      <div>
                        <div className="text-sm font-semibold text-indigo-600 mb-1">
                          🔄 Prática Mista
                        </div>
                        <div className="text-sm text-gray-600 mb-2">
                          Dificuldade: {day.difficulty}
                        </div>
                        <div className="text-sm text-gray-600 italic">
                          💡 {day.tip}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Priority Topics */}
            {studyPlan.priority_topics && studyPlan.priority_topics.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4">
                  🔥 Tópicos Prioritários
                </h3>
                <div className="space-y-2">
                  {studyPlan.priority_topics.map((topic, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-red-50 rounded">
                      <span className="font-semibold text-gray-800">
                        {index + 1}. {topic.disciplina} - {topic.topico}
                      </span>
                      <span className="text-red-600 font-bold">
                        {topic.accuracy.toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'prediction' && prediction && prediction.status === 'success' && (
          <div className="space-y-6">
            {/* Prediction Overview */}
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">
                🎯 Previsão de Desempenho
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
                <div>
                  <div className="text-6xl font-bold text-indigo-600 mb-2">
                    {prediction.estimated_score}
                  </div>
                  <div className="text-gray-600">Nota Estimada (0-100)</div>
                </div>
                <div>
                  <div className="text-6xl font-bold text-green-600 mb-2">
                    {prediction.approval_probability}%
                  </div>
                  <div className="text-gray-600">Probabilidade de Aprovação</div>
                </div>
              </div>

              {/* Status Badge */}
              <div className="inline-block px-6 py-3 rounded-full text-white font-bold text-lg mb-4">
                {prediction.performance_status === 'excellent' && (
                  <span className="bg-green-600">🌟 Excelente</span>
                )}
                {prediction.performance_status === 'good' && (
                  <span className="bg-blue-600">👍 Bom</span>
                )}
                {prediction.performance_status === 'borderline' && (
                  <span className="bg-yellow-600">⚠️ No Limite</span>
                )}
                {prediction.performance_status === 'needs_improvement' && (
                  <span className="bg-red-600">📚 Precisa Melhorar</span>
                )}
              </div>
            </div>

            {/* Recommendation */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                💡 Recomendação Personalizada
              </h3>
              <p className="text-gray-700 text-lg">
                {prediction.recommendation}
              </p>
            </div>

            {/* Areas Summary */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h4 className="font-bold text-gray-800 mb-3">
                  ⚠️ Áreas Fracas
                </h4>
                <div className="text-4xl font-bold text-red-600">
                  {prediction.weak_areas}
                </div>
                <div className="text-gray-600 mt-2">
                  Tópicos que precisam de atenção
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <h4 className="font-bold text-gray-800 mb-3">
                  ✅ Áreas Fortes
                </h4>
                <div className="text-4xl font-bold text-green-600">
                  {prediction.strong_areas}
                </div>
                <div className="text-gray-600 mt-2">
                  Tópicos dominados
                </div>
              </div>
            </div>

            {/* Action Button */}
            <div className="bg-indigo-50 rounded-lg p-6 text-center">
              <h4 className="font-bold text-gray-800 mb-4">
                Pronto para melhorar?
              </h4>
              <button
                onClick={() => navigate('/simulados')}
                className="bg-indigo-600 text-white px-8 py-3 rounded-lg hover:bg-indigo-700 font-semibold"
              >
                Fazer Simulado Personalizado
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
