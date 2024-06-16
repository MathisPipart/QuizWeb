<template>
	<div class="modal" @keydown.esc="closeModal" @click.self="closeModal" tabindex="0">
		<div class="modal-content">
			<h2>Are you sure?</h2>
			<div class="button-group">
				<button @click="closeModal" class="cancel-button">Cancel</button>
				<button @click="confirmDelete" class="delete-button">Yes</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "DeleteModal",
	methods: {
		closeModal() {
			this.$emit("close");
		},
		confirmDelete() {
			this.$emit("confirm");
		},
	},
	mounted() {
		this.$el.focus();
	},
};
</script>

<style>
button.delete-button {
	padding: 10px 20px;
	background-color: var(--vt-c-important);
	color: var(--vt-c-accent-text);
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

button.delete-button:hover {
	background-color: var(--vt-c-important-light);
}
</style>
