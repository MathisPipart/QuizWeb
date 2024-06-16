<template>
	<div v-if="!quizFinished">
		<h1>Hyrule Quiz</h1>
		<div class="BoxInfo">
			<h4 class="Joueur">{{ playerName }}</h4>
			<h4 class="Question">{{ currentQuestionPosition + 1 }} / {{ totalNumberOfQuestion }}</h4>
			<h4 class="Score">Score: {{ score }}</h4>
		</div>
		<div class="BoxQuestion">
			<div class="question-wrapper">
				<QuestionDisplay :currentQuestion="currentQuestion" @click-on-answer="handleAnswerClicked" />
			</div>
		</div>
	</div>
</template>

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

	selectedAnswersIndex.value.push(selectedAnswerIndex + 1);

	if (currentQuestionPosition.value < questions.value.length - 1) {
		setTimeout(() => {
			currentQuestionPosition.value++;
			loadQuestionByPosition(currentQuestionPosition.value);
		}, 1000);
	} else {
		setTimeout(() => {
			endQuiz();
		}, 1000);
	}
};

const endQuiz = async () => {
	quizFinished.value = true;
	participationStorageService.saveParticipationScore(score.value);
	await api.quiz.participation.add({
		playerName: playerName.value,
		answers: selectedAnswersIndex.value
	});

	registeredScores.value = await fetchRegisteredScores();
	registeredScores.value = getTop5Scores(registeredScores.value);

	await router.push({ path: '/', query: { showResults: true, score: score.value, player: playerName.value } });
};
</script>

<style scoped>
/* Container for the question module */
.BoxQuestion {
	position: relative;
	background-color: var(--color-background-soft);
	border-radius: 5px;
	padding: 20px;
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	max-width: 800px;
	margin: 20px auto;
	text-align: center;
	width: 90%;
}

/* Container for the score module */
.BoxInfo {
	position: relative;
	background-color: var(--color-background-soft);
	border-radius: 5px;
	padding: 20px;
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	max-width: 800px;
	/* Match the max width of the question box */
	margin: 20px auto;
	/* Center the box */
	text-align: center;
	width: 90%;
	/* Make it responsive */
}

/* Responsive adjustments for the score and question containers */
@media (max-width: 768px) {

	.BoxInfo,
	.BoxQuestion {
		width: 100%;
	}
}

@media (max-width: 480px) {
	.BoxQuestion {
		padding: 10px;
		font-size: 0.9rem;
	}

	.BoxInfo {
		padding: 10px;
		margin-bottom: 20px;
	}
}

.question-wrapper {
	width: 100%;
	max-width: 800px;
	margin-top: 2rem;
	padding: 0 10px;
	/* Add some padding for smaller screens */
}

.Joueur,
.Question,
.Score {
	text-align: center;
	padding: 10px 0;
	margin: 0;
}
</style>