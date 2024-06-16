<template>
	<div class="modal-overlay" @click.self="closeModal" @keydown.esc="closeModal" tabindex="0">
		<div class="modal-content">
			<div class="form-group">
				<label class="form-label">Title</label>
				<input type="text" v-model="editableQuestion.title" class="form-input"
					:class="{ 'has-error': v$.editableQuestion.title.$error }" />
			</div>
			<div class="form-group">
				<label class="form-label">Question</label>
				<input v-model="editableQuestion.text" class="form-textarea"
					:class="{ 'has-error': v$.editableQuestion.text.$error }" />
			</div>
			<div class="form-group">
				<label class="form-label">Image</label>
				<input type="file" @change="uploadImage" class="form-input-file" />
				<img v-if="editableQuestion.image" :src="editableQuestion.image" alt="Question Image"
					class="question-image" />
			</div>
			<div class="answers-container">
				<div v-for="(answer, index) in editableQuestion.possibleAnswers" :key="index"
					class="answer-edit form-group">
					<label class="form-label answer-label">Answer {{ index + 1 }}</label>
					<div class="answer-row">
						<input type="checkbox" v-model="answer.isCorrect" @change="setCorrectAnswer(index)"
							class="input-checkbox" />
						<input type="text" v-model="answer.text" class="form-input answer-input" />
						<button class="delete-button" @click="removeAnswer(index)">
							Delete
						</button>
					</div>
				</div>
			</div>

			<div class="button-group">
				<button @click="addAnswer" class="add-answer-button">Add Answer</button>
				<button @click="saveChanges" class="save-button">Save</button>
			</div>
		</div>
	</div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";

export default {
	name: "QuestionModal",
	props: {
		question: {
			type: Object,
			required: true,
		},
	},
	data() {
		return {
			editableQuestion: JSON.parse(JSON.stringify(this.question)),
		};
	},
	mounted() {
		const defaultImage = "/src/assets/default-image.png";
		this.editableQuestion.image = this.editableQuestion.image || defaultImage;
		this.$el.focus();
	},
	setup() {
		return { v$: useVuelidate() };
	},
	validations() {
		return {
			editableQuestion: {
				title: { required },
				text: { required },
				possibleAnswers: {
					$each: {
						text: { required },
					},
				},
			},
		};
	},
	methods: {
		uploadImage(event) {
			const file = event.target.files[0];
			if (file) {
				const reader = new FileReader();
				reader.onload = (e) => {
					this.editableQuestion.image = e.target.result;
				};
				reader.readAsDataURL(file);
			}
		},
		setCorrectAnswer(index) {
			this.editableQuestion.possibleAnswers.forEach((answer, i) => {
				answer.isCorrect = i === index;
			});
		},
		removeAnswer(index) {
			this.editableQuestion.possibleAnswers.splice(index, 1);
		},
		addAnswer() {
			this.editableQuestion.possibleAnswers.push({
				text: "",
				isCorrect: false,
			});
		},
		saveChanges() {
			this.v$.$validate();

			if (this.v$.$error) {
				return;
			}

			this.$emit("save", JSON.parse(JSON.stringify(this.editableQuestion)));
		},
		closeModal() {
			this.$emit("close");
		},
	},
	watch: {
		question: {
			handler(newQuestion) {
				this.editableQuestion = JSON.parse(JSON.stringify(newQuestion));
			},
			deep: true,
			immediate: true,
		},
	},
};
</script>

<style scoped>
* {
	box-sizing: border-box;
	margin: 0;
	padding: 0;
}

.modal-overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0.5);
	backdrop-filter: blur(5px);
	display: flex;
	justify-content: center;
	align-items: center;
	z-index: 1000;
}

.modal-content {
	background-color: var(--color-background-soft);
	padding: 20px;
	border-radius: 5px;
	width: 90%;
	max-width: 800px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	position: relative;
	max-height: 90vh;
	display: flex;
	flex-direction: column;
}

.form-group {
	margin-bottom: 20px;
}

.form-label {
	display: block;
	margin-bottom: 5px;
	color: var(--color-text-muted);
	font-weight: bold;
	text-align: left;
}

.form-input,
.form-textarea,
.form-input-file {
	width: 100%;
	border-radius: 5px;
	border: none;
	background-color: var(--color-background-mute);
	color: var(--color-text);
	padding: 10px;
	outline: none;
}

.form-input:focus,
.form-textarea:focus,
.form-input-file:focus {
	box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

.form-textarea {
	resize: vertical;
	height: 50px;
}

.has-error {
	border-color: var(--vt-c-important);
}

.answers-container {
	display: flex;
	flex-wrap: wrap;
	gap: 20px;
	max-height: 300px;
	overflow-y: auto;
	flex-grow: 1;
}

.answer-edit {
	flex: 1 1 calc(50% - 20px);
}

.answer-label {
	margin-bottom: 5px;
	text-align: left;
}

.answer-row {
	display: flex;
	align-items: center;
	gap: 0;
}

.answer-input {
	flex-grow: 1;
	border-radius: 0;
	height: 50px;
}

.input-checkbox {
	width: 30px;
	height: 50px;
	border-radius: 3px;
	cursor: pointer;
	appearance: none;
	background-color: var(--vt-c-tertiary);
	border-radius: 5px 0 0 5px;
	flex-grow: 1;
}

.input-checkbox:checked {
	background-color: var(--vt-c-primary);
}

.delete-button {
	background-color: var(--vt-c-important);
	color: var(--vt-c-accent-text);
	border: none;
	border-radius: 0 5px 5px 0;
	padding: 10px;
	cursor: pointer;
	height: 50px;
}

.delete-button:hover {
	background-color: var(--vt-c-important-light);
}

.button-group {
	display: flex;
	justify-content: space-between;
	gap: 10px;
	margin-top: 20px;
}

.add-answer-button,
.save-button {
	flex: 1;
	padding: 15px;
	color: var(--vt-c-accent-text);
	border: none;
	border-radius: 5px;
	font-size: 18px;
	cursor: pointer;
}

.add-answer-button {
	background-color: var(--vt-c-tertiary);
}

.add-answer-button:hover {
	background-color: var(--vt-c-tertiary-light);
}

.save-button {
	background-color: var(--vt-c-primary);
}

.save-button:hover {
	background-color: var(--vt-c-primary-light);
}

.question-image {
	width: 100%;
	max-height: 200px;
	object-fit: cover;
	margin-top: 10px;
	border-radius: 5px;
}
</style>
