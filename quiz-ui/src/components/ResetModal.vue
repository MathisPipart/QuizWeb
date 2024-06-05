<template>
	<div class="modal" @keydown.esc="closeModal" @click.self="closeModal" tabindex="0">
		<div class="modal-content">
			<h2>Are you sure you want to reset the leaderboard?</h2>
			<div class="button-group">
				<button @click="closeModal" class="cancel-button">Cancel</button>
				<button @click="confirmReset" class="reset-button">Yes</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'ResetModal',
	methods: {
		closeModal() {
			this.$emit('close');
		},
		confirmReset() {
			this.$emit('confirm');
		}
	},
	mounted() {
		this.$el.focus();
	}
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

.modal-content {
	background-color: #fff;
	padding: 20px;
	border: 1px solid #888;
	width: 80%;
	max-width: 400px;
	text-align: center;
	position: relative;
	border-radius: 5px;
	box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.button-group {
	display: flex;
	justify-content: space-between;
	gap: 10px;
}

button.cancel-button {
	padding: 10px 20px;
	background-color: #77dd77;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

button.cancel-button:hover {
	background-color: #90ee90;
}

button.reset-button {
	padding: 10px 20px;
	background-color: #f94f4f;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

button.reset-button:hover {
	background-color: #f76a6a;
}
</style>