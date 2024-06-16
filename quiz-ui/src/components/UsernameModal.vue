<template>
	<div class="modal" @keydown.esc="closeModal" @click.self="closeModal" tabindex="0">
		<form @submit.prevent="launchQuiz">
			<label for="username">Username</label>
			<input type="text" id="username" v-model="username" placeholder="Username" autocorrect="off"
				autocapitalize="none" required ref="usernameInput" autocomplete="off" />
			<div class="submit-errors" v-if="error">
				<div>{{ errorMessageFromCode }}</div>
			</div>

			<div class="button-group">
				<button type="button" @click="closeModal" class="cancel-button">Cancel</button>
				<input type="submit" value="Start Quiz!" />
			</div>
		</form>
	</div>
</template>

<script>
import { useUserStore } from '@/stores/userStores';
import participationStorageService from "@/services/ParticipationStorageService";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";

export default {
	name: 'UsernameModal',
	setup() {
		const store = useUserStore();
		return { store, v$: useVuelidate() };
	},
	data() {
		return {
			username: '',
			error: false,
		};
	},
	mounted() {
		this.username = '';
		this.error = false;
		this.$refs.usernameInput.focus();
	},
	computed: {
		errorMessageFromCode() {
			switch (this.error) {
				case 'ERR_BAD_REQUEST':
					return 'Incorrect username';
				default:
					return 'An error occurred';
			}
		},
	},
	methods: {
		launchQuiz() {
			this.v$.$validate();

			if (this.v$.$error) {
				return;
			}
			console.log("Launch new quiz with", this.username);
			participationStorageService.savePlayerName(this.username);
			this.$router.push('/questions');
			this.closeModal();
		},
		closeModal() {
			this.$emit('close');
		},
	},
	validations() {
		return {
			username: { required },
		};
	},
};
</script>

<style>
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

.modal form {
	background-color: var(--color-background-soft);
	padding: 20px;
	width: 80%;
	max-width: 400px;
	text-align: center;
	position: relative;
	border-radius: 5px;
	box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal form label {
	display: block;
	margin-bottom: 10px;
	font-weight: bold;
}

.modal form input[type="text"] {
	width: calc(100% - 22px);
	padding: 10px;
	margin-bottom: 20px;
	border-radius: 5px;
	background-color: var(--color-background-mute);
	color: var(--color-text);
	border: none;
	text-align: center;
}

.modal form input[type="text"]:focus {
	outline: none;
	box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

.modal form .button-group {
	display: flex;
	justify-content: center;
	gap: 10px;
}

.modal form input[type="submit"],
.modal form button.cancel-button {
	padding: 10px 20px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

.modal form input[type="submit"] {
	background-color: var(--vt-c-primary);
	color: var(--vt-c-accent-text);
}

.modal form input[type="submit"]:hover {
	background-color: var(--vt-c-primary-light);
}

.modal form input[type="submit"]:disabled {
	background-color: var(--color-background-mute);
}

.modal form button.cancel-button {
	background-color: var(--vt-c-important);
	color: var(--vt-c-accent-text);
}

.modal form button.cancel-button:hover {
	background-color: var(--vt-c-important-light);
}

.modal .submit-errors {
	color: var(--vt-c-important);
	margin-bottom: 20px;
}

.modal .has-error {
	border-color: var(--vt-c-important);
}
</style>