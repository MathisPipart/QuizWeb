<script setup>
import { ref, onMounted } from 'vue';
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
		score: score.value,
		answers: selectedAnswersIndex.value
	});

	// Recharger les scores après avoir ajouté la participation
	registeredScores.value = await fetchRegisteredScores();
	registeredScores.value = getTop5Scores(registeredScores.value);
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
	<div v-else>
		<h1>Quiz Finished!</h1>
		<p class="Thanks">Thank you for participating in the quiz, {{ playerName }}. Your score is: {{ score }} / {{
			totalNumberOfQuestion }}</p>
        <div class="Boite">
            <h2>Meilleurs scores des autres joueurs</h2>
            <div class="scoreboard">
                <div v-for="(playerScore, index) in registeredScores" :key="playerScore.playerName" :class="{
                    first: index === 0,
                    second: index === 1,
                    third: index === 2,
                    fourth: index === 3,
                    fifth: index === 4,
                    other: index >= 5,
                }">
                    <span class="position">{{ index + 1 }}</span>
                    <span class="name">{{ playerScore.playerName }}</span>
                    <span class="score">{{ playerScore.score }}</span>
                </div>
            </div>
            <!-- Bouton pour revenir à la page Home -->
            <RouterLink to="/" class="home-button">
                Revenir à la page Home
            </RouterLink>
        </div>
	</div>
</template>


<style scoped>
.BoxQuestion{
	position: relative;
	background-color: white;
	border-radius: 15px;
	padding: 20px;
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	max-width: 800px;
	margin: 0 auto;
	text-align: center;
}

.BoxInfo {
	position: relative;
	width: 250px;
	border-radius: 15px;
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	margin-right: 2%;
	float: right;
	text-align: center;
}

.question-wrapper {
	width: 100%;
	max-width: 800px;
	margin-top: 2rem;
}

.home-button {
	display: inline-block;
	margin-top: 2rem;
	padding: 0.5rem 1rem;
	background-color: #41b883;
	color: white;
	text-decoration: none;
	border-radius: 5px;
	font-weight: bold;
	text-align: center;
}

.home-button:hover {
	background-color: #3a9d70;
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
.Score{
	text-align: center;
	margin-right: 2%;
	padding-bottom: 5%;
}
.Thanks{
	text-align: center;
}
</style>
<style src="../css/Scores.css"></style>
