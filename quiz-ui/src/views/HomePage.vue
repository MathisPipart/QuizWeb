<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const scores = ref([]);

onMounted(async () => {
	const response = await api.quiz.get();
	const allScores = response.data.scores;

	// Sort scores in descending order
	allScores.sort((a, b) => b.score - a.score);

	// Take the top 5 scores
	scores.value = allScores.slice(0, 5);
});
</script>

<template>
	<h1>Home page</h1>
	<br />
	<h2>Classement</h2>
	<div class="scoreboard">
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
	<br />
	<router-link to="/new-quiz" class="start-quiz-link">Démarrer le quiz !</router-link>
</template>

<style scoped>
.start-quiz-link {
	display: inline-block;
	padding: 0.5rem 1rem;
	background-color: #41b883;
	color: white;
	text-decoration: none;
	border-radius: 5px;
	font-weight: bold;
	text-align: center;
	transition: background-color 0.3s;
}

.start-quiz-link:hover {
	background-color: #3a9d70;
}
</style>

<style src="../css/Scores.css"></style>
