<script>
import participationStorageService from "@/services/ParticipationStorageService";
import { useRouter } from 'vue-router';

export default {
	data() {
		return {
			username: ''
		}
	},
	mounted() {
		this.$refs.usernameInput.focus();
	},
	setup() {
		const router = useRouter();
		return { router };
	},
	methods: {
		launchNewQuiz() {
			console.log("Launch new quiz with", this.username);
			participationStorageService.savePlayerName(this.username);
			// const playerName = participationStorageService.getPlayerName();
			this.router.push('/questions');
		}
	}
}
</script>

<template>
	<div class="new-quiz">
		<h1>Lancement du Quiz</h1>
		<br>
		<form class="box" @submit.prevent="launchNewQuiz">
			<p>What's your name?</p>
			<input type="text" v-model="username" placeholder="Username" class="form-control" ref="usernameInput"
				required>
			<button type="submit" class="green-button" @click="launchNewQuiz">Start Quiz !</button>
		</form>
	</div>
</template>

<style>
.box {
	position: relative;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	max-width: 800px;
	max-height: 250px;
	padding: 20px;
	border-radius: 5px;
	margin: 0 auto;
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	background-color: var(--color-background-soft);
}

h1 {
	font-size: 2rem;
	font-weight: bold;
	color: var(--color-text);
}

p {
	font-size: 1.5rem;
	color: var(--color-text);
}

.form-control {
	width: 20%;
	padding: 5px;
	margin: 10px;
	text-align: center;
	width: 50%;
	background-color: var(--color-background-mute);
	color: var(--color-text);
	border: none;
}

.form-control:focus {
	outline: none;
	box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
	background-color: var(--color-background-mute);
	color: var(--color-text);
}

.green-button {
	margin-top: 10px;
	display: inline-block;
	padding: 0.5rem 1rem;
	background-color: var(--vt-c-primary);
	color: var(--vt-c-accent-text);
	text-decoration: none;
	border-radius: 5px;
	font-weight: bold;
	text-align: center;
	transition: background-color 0.3s;
	border-color: transparent;
}

.green-button:hover {
	background-color: var(--vt-c-primary-light);
}
</style>