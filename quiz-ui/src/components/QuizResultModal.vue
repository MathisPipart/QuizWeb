<template>
	<div class="modal" @keydown.esc="closeModal" @click.self="closeModal" tabindex="0">
		<div class="modal-content">
			<h1>Quiz Result</h1>
			<!-- <p class="Thanks">Merci d'avoir participé à ce quiz, {{ playerName }}.<br> Votre score est de : {{ score }}
				/ {{ totalNumberOfQuestion }}</p> -->
			<p class="Thanks">Thank you for participating in this quiz, {{ playerName }}.<br> Your score is : {{ score
				}}/{{ totalNumberOfQuestion }}</p>
			<button @click="closeModal" class="close-button" ref="closeButton">Close</button>
		</div>
	</div>
</template>

<script>

export default {
	name: 'QuizResultModal',
	props: {
		playerName: String,
		score: Number,
		totalNumberOfQuestion: Number,
		registeredScores: Array,
	},
	methods: {
		closeModal() {
			this.$emit('closeQuizResultModal');
		},
	},
	mounted() {
		this.$refs.closeButton.focus();
	},
}

</script>

<style scoped>
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
	outline: none;
}

.close-button:hover {
	background-color: var(--vt-c-primary-light);
}
</style>
