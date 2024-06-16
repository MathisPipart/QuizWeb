<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import QuizResultModal from '@/components/QuizResultModal.vue';
import UsernameModal from '@/components/UsernameModal.vue';

const scores = ref([]);
const questionCount = ref(0);
const showResultsModal = ref(false);
const playerName = ref('');
const playerScore = ref(0);
const showLaunchModal = ref(false);

const route = useRoute();
const router = useRouter();

onMounted(async () => {
	const response = await api.quiz.get();
	const allScores = response.data.scores;
	questionCount.value = response.data.size;

	allScores.sort((a, b) => b.score - a.score);
	scores.value = allScores.slice(0, 5);

	if (route.query.showResults) {
		playerName.value = route.query.player;
		playerScore.value = route.query.score;
		showResultsModal.value = true;
	}
});

watch(route, (newRoute) => {
	if (newRoute.query.showResults) {
		playerName.value = newRoute.query.player;
		playerScore.value = newRoute.query.score;
		showResultsModal.value = true;
	}
});

const closeModal = () => {
	showResultsModal.value = false;
	router.replace({ query: null });
};

const closeUsernameModal = () => {
	showLaunchModal.value = false;
};

</script>

<template>
	<h1>Quizzer</h1>
	<br />
	<div class="Boite">
		<h2>Leaderboard</h2>
		<div class="scoreboard" v-if="scores.length > 0">
			<div v-for="(scoreEntry, index) in scores" :key="scoreEntry.playerName" :class="{
				first: index === 0,
				second: index === 1,
				third: index === 2,
				other: index >= 3,
			}">
				<span class="position">{{ index + 1 }}</span>
				<span class="name">{{ scoreEntry.playerName }}</span>
				<span class="score">{{ scoreEntry.score }}</span>
			</div>
		</div>
		<p class="participation-count" v-else>No participation yet</p>
		<br />
		<button class="start-quiz-link" @click="showLaunchModal = true" v-if="questionCount > 0">Start Quiz
			!</button>
		<p class="simili-button" v-else>No questions</p>
	</div>

	<QuizResultModal v-if="showResultsModal" :playerName="playerName" :score="playerScore"
		:totalNumberOfQuestion="questionCount" :registeredScores="scores" @closeQuizResultModal="closeModal" />
	<UsernameModal v-if="showLaunchModal" @close="closeUsernameModal" />
</template>

<style scoped>
body {
	font-family: 'Arial', sans-serif;
	line-height: 1.6;
}

h1,
h2 {
	text-align: center;
}

.Boite {
	width: 100%;
	max-width: 900px;
	margin: 0 auto;
	padding: 1rem;
	background-color: var(--color-background-soft);
	border-radius: 5px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	transition: all 0.3s ease;
	padding: 20px;
	text-align: center;
}

.start-quiz-link {
	display: inline-block;
	width: 100%;
	max-width: 250px;
	margin: 0.5rem auto;
	padding: 0.5rem 1rem;
	background-color: var(--vt-c-primary);
	color: var(--vt-c-accent-text);
	text-decoration: none;
	border-radius: 5px;
	font-weight: bold;
	text-align: center;
	transition: background-color 0.3s;
	border: none;
	cursor: pointer;
}

.start-quiz-link:hover {
	background-color: var(--vt-c-primary-light);
}

.simili-button {
	display: inline-block;
	width: 100%;
	max-width: 250px;
	margin: 0.5rem auto;
	padding: 0.5rem 1rem;
	background-color: var(--vt-c-greyed-out);
	color: var(--vt-c-greyed-out-text);
	border-radius: 5px;
	font-weight: bold;
	text-align: center;
}

.simili-button:hover {
	background-color: var(--vt-c-greyed-out-light);
	cursor: not-allowed;
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

.participation-count {
	margin-top: 1rem;
	font-size: 1.2em;
	text-align: center;
}

/* Media Queries */
@media (max-width: 768px) {
	.Boite {
		width: 95%;
		padding: 1rem;
	}

	.scoreboard {
		gap: 0.5rem;
	}

	.start-quiz-link,
	.simili-button {
		width: 100%;
	}

	.modal-content {
		width: 95%;
	}
}

@media (max-width: 480px) {
	.Boite {
		width: 100%;
		padding: 0.5rem;
	}

	.start-quiz-link,
	.simili-button {
		width: 100%;
		font-size: 0.9rem;
		padding: 0.5rem 0.8rem;
	}

	.modal-content {
		width: 90%;
		padding: 10px;
	}
}
</style>