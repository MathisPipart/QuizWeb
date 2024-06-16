<template>
	<div>
		<h2 class="question-title">{{ currentQuestion.title }}</h2>
		<h2 class="currentQuestion">{{ currentQuestion.text }}</h2>
		<div class="image-container" v-if="currentQuestion.image">
			<img :src="currentQuestion.image" alt="Question image" class="question-image">
		</div>
		<div class="options-container">
			<div class="question-option" v-for="(option, index) in currentQuestion.options" :key="index"
				@click="handleOptionClick(index)" :class="{
					correct: selectedOption === index && option === currentQuestion.correctAnswer,
					incorrect: selectedOption === index && option !== currentQuestion.correctAnswer
				}">
				{{ option }}
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		currentQuestion: {
			type: Object,
			required: true
		}
	},
	data() {
		return {
			selectedOption: null
		};
	},
	methods: {
		handleOptionClick(index) {
			if (this.selectedOption === null) {
				this.selectedOption = index;
				this.$emit('click-on-answer', index);
			}
		}
	},
	watch: {
		currentQuestion() {
			this.selectedOption = null;
		}
	}
}
</script>

<style scoped>
/* Styling for the question title */
.question-title {
	font-weight: bold;
	margin-bottom: 15px;
	/* Increased margin for better spacing */
	text-align: center;
}

.currentQuestion {
	text-align: center;
	margin-top: 20px;
	/* Added margin to create space above the text */
	margin-bottom: 4%;
	font-size: 1.2rem;
}

.image-container {
	width: 100%;
	max-width: 100%;
	height: auto;
	display: flex;
	justify-content: center;
	align-items: center;
	margin-bottom: 20px;
	overflow: hidden;
}

.question-image {
	width: 100%;
	max-height: 300px;
	object-fit: cover;
	object-position: center;
	border-radius: 5px;
}

.options-container {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 0.5rem;
	max-width: 100%;
	width: 100%;
}

.question-option {
	cursor: pointer;
	padding: 1rem;
	background-color: var(--vt-c-tertiary);
	border-radius: 5px;
	transition: background-color 0.3s;
	text-align: center;
	color: var(--vt-c-accent-text);
	word-wrap: break-word;
	font-size: 1rem;
}

/* Full width for single options on smaller screens */
.options-container> :nth-child(odd):last-child {
	grid-column: span 2;
}

.question-option:hover {
	background-color: var(--vt-c-tertiary-light);
}

.question-option.correct {
	background-color: var(--vt-c-primary);
}

.question-option.incorrect {
	background-color: var(--vt-c-important);
}

/* Responsive adjustments for options */
@media (max-width: 768px) {
	.options-container {
		grid-template-columns: 1fr;
	}

	.question-option {
		padding: 0.5rem;
		font-size: 0.9rem;
	}
}

@media (max-width: 480px) {
	.options-container {
		grid-template-columns: 1fr;
	}

	.question-option {
		padding: 0.5rem;
		font-size: 0.8rem;
	}
}
</style>