<template>
	<div class="modal" @keydown.esc="closeModal" @click.self="closeModal" tabindex="0">
		<div class="modal-content">
			<h2>Are you sure?</h2>
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
	background-color: var(--color-background-soft);
	padding: 20px;
	width: 80%;
	max-width: 400px;
	text-align: center;
	position: relative;
	border-radius: 10px;
	box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.button-group {
	display: flex;
	justify-content: space-between;
	gap: 10px;
}

button.cancel-button {
	padding: 10px 20px;
	background-color: var(--vt-c-primary);
	color: var(--vt-c-accent-text);
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

button.cancel-button:hover {
	background-color: var(--vt-c-primary-light);
}

button.reset-button {
	padding: 10px 20px;
	background-color: var(--vt-c-important);
	color: var(--vt-c-accent-text);
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

button.reset-button:hover {
	background-color: var(--vt-c-important-light);
}
</style>