<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const scores = ref([]);
const questionCount = ref(0);

onMounted(async () => {
	const response = await api.quiz.get();
	const allScores = response.data.scores;
	questionCount.value = response.data.size;

	// Sort scores in descending order
	allScores.sort((a, b) => b.score - a.score);
	// Take the top 5 scores
	scores.value = allScores.slice(0, 5);
});
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
				fourth: index === 3,
				fifth: index === 4,
				other: index >= 5,
			}">
				<span class="position">{{ index + 1 }}</span>
				<span class="name">{{ scoreEntry.playerName }}</span>
				<span class="score">{{ scoreEntry.score }}</span>
			</div>
		</div>
		<p class="participation-count" v-else>No participation yet</p>
		<br />
		<router-link to="/new-quiz" class="start-quiz-link" v-if="questionCount > 0">Start the Quiz !</router-link>
		<p class="simili-button" v-else>No questions</p>
	</div>
</template>

<style scoped>
.participation-count {
	margin-top: 1rem;
	font-size: 1.2em;
}

.start-quiz-link {
	display: inline-block;
	padding: 0.5rem 1rem;
	background-color: var(--vt-c-primary);
	color: var(--vt-c-accent-text);
	text-decoration: none;
	border-radius: 5px;
	font-weight: bold;
	text-align: center;
	transition: background-color 0.3s;
}

.start-quiz-link:hover {
	background-color: var(--vt-c-primary-light);
}

.simili-button {
	font-size: 1rem;
	display: inline-block;
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
</style>

<style src="../css/scores.css"></style>
