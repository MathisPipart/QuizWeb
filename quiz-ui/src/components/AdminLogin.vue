<template>
	<div class="modal" @keydown.esc="closeModal" @click.self="closeModal" tabindex="0">
		<form @submit.prevent="login">
			<label for="password">Password:</label>
			<input type="password" id="password" v-model="password" placeholder="Password" autocorrect="off"
				autocapitalize="none" required />

			<div class="submit-errors" v-if="error">
				<div>{{ errorMessageFromCode }}</div>
			</div>

			<div class="button-group">
				<button type="button" @click="closeModal" class="cancel-button">Cancel</button>
				<input type="submit" value="Login" />
			</div>
		</form>
	</div>
</template>

<script>
import { useUserStore } from '@/stores/userStores';

export default {
	name: 'AdminLogin',
	setup() {
		const store = useUserStore();
		return { store };
	},
	data() {
		return {
			password: '',
			error: false,
		};
	},
	mounted() {
		this.password = '';
		this.error = false;
		this.$el.focus();
	},
	computed: {
		errorMessageFromCode() {
			switch (this.error) {
				case 'ERR_BAD_REQUEST':
					return 'Incorrect password';
				default:
					return 'An error occurred';
			}
		},
	},
	methods: {
		async login() {
			try {
				await this.store.login(this.password);
				this.closeModal();
			} catch (error) {
				console.error(error);
				this.error = error.code;
			}
		},
		closeModal() {
			this.$emit('close');
		},
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
	background-color: #fff;
	padding: 20px;
	border: 1px solid #888;
	width: 80%;
	max-width: 400px;
	text-align: center;
	position: relative;
	border-radius: 10px;
	box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal form label {
	display: block;
	margin-bottom: 10px;
	font-weight: bold;
}

.modal form input[type="password"] {
	width: calc(100% - 22px);
	padding: 10px;
	margin-bottom: 20px;
	border: 1px solid #ccc;
	border-radius: 5px;
}

.modal form .button-group {
	display: flex;
	justify-content: center;
	gap: 10px;
	/* Add gap between buttons */
}

.modal form input[type="submit"],
.modal form button.cancel-button {
	padding: 10px 20px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

.modal form input[type="submit"] {
	background-color: #77DD77;
	color: white;
}

.modal form input[type="submit"]:hover {
	background-color: #90EE90;
}

.modal form input[type="submit"]:disabled {
	background-color: #ccc;
}

.modal form button.cancel-button {
	background-color: #f94f4f;
	color: white;
}

.modal form button.cancel-button:hover {
	background-color: #f76a6a;
}

.modal .submit-errors {
	color: red;
	margin-bottom: 20px;
}

.modal .has-error {
	border-color: red;
}
</style>