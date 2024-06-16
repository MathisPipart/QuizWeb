<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import participationStorageService from '@/services/ParticipationStorageService';
import QuestionDisplay from '../views/QuestionDisplay.vue';

const playerName = ref(participationStorageService.getPlayerName() || 'Player');
const currentQuestion = ref({});
const currentQuestionPosition = ref(0);
const totalNumberOfQuestion = ref(0);
const quizFinished = ref(false);
const score = ref(0);
const registeredScores = ref([]);
const questions = ref([]);
const nbQuestions = ref(0);
const selectedAnswersIndex = ref([]);

const router = useRouter();

onMounted(async () => {
	try {
		const response = await api.quiz.get();
		nbQuestions.value = response.data.size;
	} catch (error) {
		console.error("Error fetching quiz data: ", error);
	}

	totalNumberOfQuestion.value = nbQuestions.value;
	await fetchQuestions();

	loadQuestionByPosition(currentQuestionPosition.value);
	registeredScores.value = await fetchRegisteredScores();
	registeredScores.value = getTop5Scores(registeredScores.value);
});

const fetchQuestions = async () => {
	for (let i = 1; i <= nbQuestions.value; i++) {
		try {
			const response = await api.quiz.question.getByPosition(i);
			const rawQuestion = response.data;

			const formattedQuestion = {
				id: rawQuestion.id,
				title: rawQuestion.title,
				text: rawQuestion.text,
				options: rawQuestion.possibleAnswers.map(answer => answer.text),
				correctAnswer: rawQuestion.possibleAnswers.find(answer => answer.isCorrect).text,
				image: rawQuestion.image
			};

			questions.value.push(formattedQuestion);
		} catch (error) {
			console.error("Error fetching question data: ", error);
		}
	}
};

const fetchRegisteredScores = async () => {
	const response = await api.quiz.get();
	return response.data.scores;
};

const getTop5Scores = (scores) => {
	return scores.sort((a, b) => b.score - a.score).slice(0, 5);
};

const loadQuestionByPosition = (position) => {
	if (position < questions.value.length) {
		currentQuestion.value = questions.value[position];
	}
};

const handleAnswerClicked = (selectedAnswerIndex) => {
	const selectedAnswer = currentQuestion.value.options[selectedAnswerIndex];
	if (selectedAnswer === currentQuestion.value.correctAnswer) {
		score.value++;
	}

	// Enregistre l'index de la réponse sélectionnée, en ajoutant 1 pour commencer à 1
	selectedAnswersIndex.value.push(selectedAnswerIndex + 1);

	if (currentQuestionPosition.value < questions.value.length - 1) {
		setTimeout(() => {
			currentQuestionPosition.value++;
			loadQuestionByPosition(currentQuestionPosition.value);
		}, 1000); // Attendre 1 seconde avant de passer à la question suivante
	} else {
		setTimeout(() => {
			endQuiz();
		}, 1000); // Attendre 1 seconde avant de terminer le quiz
	}
};

const endQuiz = async () => {
	quizFinished.value = true;
	participationStorageService.saveParticipationScore(score.value);
	await api.quiz.participation.add({
		playerName: playerName.value,
		answers: selectedAnswersIndex.value
	});

	// Recharger les scores après avoir ajouté la participation
	registeredScores.value = await fetchRegisteredScores();
	registeredScores.value = getTop5Scores(registeredScores.value);

	// Redirect to homepage with query parameter
	await router.push({ path: '/', query: { showResults: true, score: score.value, player: playerName.value } });

	// Show modal (will be handled on the homepage)
};
</script>

<template>
	<div v-if="!quizFinished">
		<h1>{{ currentQuestion.title }}</h1>
		<br>
		<div class="BoxInfo">
			<h4 class="Joueur">{{ playerName }}</h4>
			<h4 class="Question">{{ currentQuestionPosition + 1 }} / {{ totalNumberOfQuestion }}</h4>
			<h4 class="Score">Score : {{ score }}</h4>
		</div>
		<div class="BoxQuestion">
			<div class="question-wrapper">
				<QuestionDisplay :currentQuestion="currentQuestion" @click-on-answer="handleAnswerClicked" />
			</div>
		</div>
	</div>
</template>

<style scoped>
.BoxQuestion {
	position: relative;
	background-color: var(--color-background-soft);
	border-radius: 5px;
	padding: 20px;
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	max-width: 800px;
	margin: 0 auto;
	text-align: center;
}

.BoxInfo {
	position: relative;
	width: 250px;
	border-radius: 5px;
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	margin-right: 2%;
	float: right;
	text-align: center;
	background-color: var(--color-background-soft);
}

.question-wrapper {
	width: 100%;
	max-width: 800px;
	margin-top: 2rem;
}

.Joueur {
	text-align: center;
	margin-right: 2%;
	padding-top: 5%;
}

.Question {
	text-align: center;
	margin-right: 2%;
	padding-top: 2%;
	padding-bottom: 2%;
}

.Score {
	text-align: center;
	margin-right: 2%;
	padding-bottom: 5%;
}

.Thanks {
	text-align: center;
}

.modal {
	display: flex;
	justify-content: center;
	align-items: center;
	position: fixed;
	z-index: 1;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	overflow: auto;
	background-color: rgba(0, 0, 0, 0.7);
	backdrop-filter: blur(5px);
}

.modal-content {
	background-color: var(--color-background-soft);
	padding: 20px;
	width: 80%;
	max-width: 500px;
	text-align: center;
	position: relative;
	border-radius: 5px;
	box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.close-button {
	margin-top: 20px;
	padding: 10px 20px;
	background-color: var(--vt-c-primary);
	color: var(--vt-c-accent-text);
	border: none;
	border-radius: 5px;
	cursor: pointer;
	font-weight: bold;
	text-align: center;
}

.close-button:hover {
	background-color: var(--vt-c-primary-light);
}
</style>
