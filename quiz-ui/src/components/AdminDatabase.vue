<template>

	<div class="database-container">
		<h2 class="db-title">Database Management</h2>
		<div class="database-buttons">
			<button class="empty" @click="clearDatabase">Empty</button>
			<button class="load-default" @click="initDatabase">Add Questions</button>
			<button class="load-participation" @click="loadParticipation">Add Participations</button>
		</div>
	</div>

</template>

<script>

import api from "@/api";

export default {
	name: "AdminDatabase",
	methods: {
		async clearDatabase() {
			await api.admin.database.reset();
			this.$emit("reset");
		},
		async initDatabase() {
			await api.admin.database.reset();
			for (const question of this.defaultQuestions) {
				this.convertImageToBase64(question.image)
					.then(base64 => {
						question.image = base64;
					})
					.catch(error => {
						console.error('Error converting image to base64:', error);
					});
				await api.admin.question.add(question);
			}

			this.$emit("reset");
		},
		async convertImageToBase64(imageUrl) {
			try {
				const response = await fetch(imageUrl);
				const blob = await response.blob();
				return new Promise((resolve, reject) => {
					const reader = new FileReader();
					reader.onloadend = () => {
						resolve(reader.result);
					};
					reader.onerror = reject;
					reader.readAsDataURL(blob);
				});
			} catch (error) {
				console.error('Error fetching image:', error);
				throw error;
			}
		},
		async loadParticipation() {
			const scores = [
				{
					playerName: "Alice Smith",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Bob Johnson",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Carol Williams",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "David Brown",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Emma Jones",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Frank Garcia",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Grace Miller",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Hank Davis",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Ivy Martinez",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Jack Wilson",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Kate Anderson",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Leo Thomas",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Mia Hernandez",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Noah Moore",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Olivia Martinez",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Paul Clark",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Quincy Lewis",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Rita Walker",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Steve Hall",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Tina Allen",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Uma Young",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Victor Hernandez",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Wendy King",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Xander Wright",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Yara Lopez",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Zane Scott",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Hannah Parker",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "James Adams",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Mason Baker",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Sophia Mitchell",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
				{
					playerName: "Jacob Perez",
					answers: Array.from({ length: 30 }, () => Math.floor(Math.random() * 6) + 1),
				},
			]
			for (const score of scores) {
				await api.quiz.participation.add(score);
			}
		}
	},
	data() {
		return {
			defaultQuestions: [
				{
					title: "Question 1",
					text: "Quel est le premier jeu Zelda qui permet de sauvegarder sa partie ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 1,
					possibleAnswers: [
						{ text: "The Legend of Zelda", isCorrect: true },
						{ text: "Zelda II: The Adventure of Link", isCorrect: false },
						{ text: "The Legend of Zelda: A Link to the Past", isCorrect: false },
						{ text: "The Legend of Zelda: Link's Awakening", isCorrect: false },
					],
				},
				{
					title: "Question 2",
					text: "Quel est le premier jeu Zelda en 3D ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 2,
					possibleAnswers: [
						{ text: "The Legend of Zelda: The Wind Waker", isCorrect: false },
						{ text: "The Legend of Zelda: Majora's Mask", isCorrect: false },
						{ text: "The Legend of Zelda: Ocarina of Time", isCorrect: true },
						{ text: "The Legend of Zelda: Twilight Princess", isCorrect: false },
					],
				},
				{
					title: "Question 3",
					text: "Quel est le premier jeu Zelda sur console portable ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 3,
					possibleAnswers: [
						{ text: "The Legend of Zelda: Oracle of Seasons", isCorrect: false },
						{ text: "The Legend of Zelda: Oracle of Ages", isCorrect: false },
						{ text: "The Legend of Zelda: A Link to the Past", isCorrect: false },
						{ text: "The Legend of Zelda: Link's Awakening", isCorrect: true },
					],
				},
				{
					title: "Question 4",
					text: "Quel est le premier jeu de la chronologie officielle de Zelda ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 4,
					possibleAnswers: [
						{ text: "The Legend of Zelda", isCorrect: false },
						{ text: "The Legend of Zelda: Skyward Sword", isCorrect: true },
						{ text: "The Legend of Zelda: Ocarina of Time", isCorrect: false },
						{ text: "The Legend of Zelda: A Link to the Past", isCorrect: false },
					],
				},
				{
					title: "Question 5",
					text: "Combien y a-t-il de jeux Zelda de la série principale ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 5,
					possibleAnswers: [
						{ text: "16", isCorrect: false },
						{ text: "20", isCorrect: true },
						{ text: "22", isCorrect: false },
						{ text: "27", isCorrect: false },
					],
				},
				{
					title: "Question 6",
					text: "Nintendo a développé tous les jeux Zelda de la série principale.",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 6,
					possibleAnswers: [
						{ text: "Vrai", isCorrect: false },
						{ text: "Faux", isCorrect: true },
					],
				},
				{
					title: "Question 7",
					text: "Quelle est l'année de sortie du premier jeu Zelda ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 7,
					possibleAnswers: [
						{ text: "1986", isCorrect: true },
						{ text: "1987", isCorrect: false },
						{ text: "1988", isCorrect: false },
						{ text: "1989", isCorrect: false },
					],
				},
				{
					title: "Question 8",
					text: "Lequel n'est pas un ennemi dans Zelda ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 8,
					possibleAnswers: [
						{ text: "Goomba", isCorrect: false },
						{ text: "Abeille", isCorrect: false },
						{ text: "Armos", isCorrect: false },
						{ text: "Chevalier", isCorrect: true },
					],
				},
				{
					title: "Question 9",
					text: "Quel est le Zelda le mieux noté (selon Metacritic) ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 9,
					possibleAnswers: [
						{ text: "The Legend of Zelda: Majora's Mask", isCorrect: false },
						{ text: "The Legend of Zelda: Tears of the Kingdom", isCorrect: false },
						{ text: "The Legend of Zelda: Ocarina of Time", isCorrect: true },
						{ text: "The Legend of Zelda: Breath of the Wild", isCorrect: false },
					],
				},
				{
					title: "Question 10",
					text: "Quelle console Nintendo n'a pas eu de Zelda exclusif ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 10,
					possibleAnswers: [
						{ text: "GameCube", isCorrect: false },
						{ text: "Wii U", isCorrect: true },
						{ text: "3DS", isCorrect: false },
						{ text: "SNES", isCorrect: false },
					],
				},
				{
					title: "Question 11",
					text: "Link n'a jamais parlé.",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 11,
					possibleAnswers: [
						{ text: "Vrai", isCorrect: false },
						{ text: "Faux", isCorrect: true },
					],
				},
				{
					title: "Question 12",
					text: "Combien de jeux Zelda ne sont pas sortis sur une console Nintendo ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 12,
					possibleAnswers: [
						{ text: "0", isCorrect: false },
						{ text: "3", isCorrect: true },
						{ text: "5", isCorrect: false },
						{ text: "1", isCorrect: false },
					],
				},
				{
					title: "Question 13",
					text: "Lequel n'est pas un compagnon de Link ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 13,
					possibleAnswers: [
						{ text: "Navi", isCorrect: false },
						{ text: "Tael", isCorrect: true },
						{ text: "Taya", isCorrect: false },
						{ text: "Midona", isCorrect: false },
					],
				},
				{
					title: "Question 14",
					text: "Lequel de ces jeux est un spin-off officiel ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 14,
					possibleAnswers: [
						{ text: "Cadence of Hyrule", isCorrect: true },
						{ text: "Hyrule Gladiator", isCorrect: false },
						{ text: "Tingle Chaser", isCorrect: false },
						{ text: "Zelda's Adventure", isCorrect: false },
					],
				},
				{
					title: "Question 15",
					text: "Quelle société a déjà détenu les droits sur la licence Zelda ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 15,
					possibleAnswers: [
						{ text: "Sony", isCorrect: false },
						{ text: "Microsoft", isCorrect: false },
						{ text: "Philips", isCorrect: true },
						{ text: "Sega", isCorrect: false },
						{ text: "Atari", isCorrect: false },
						{ text: "Aucune", isCorrect: false },
					],
				},
				{
					title: "Question 16",
					text: "Quel jeu est sorti un 3 mars ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 16,
					possibleAnswers: [
						{ text: "The Legend of Zelda: Twilight Princess", isCorrect: false },
						{ text: "The Legend of Zelda: Skyward Sword", isCorrect: false },
						{ text: "The Legend of Zelda: Breath of the Wild", isCorrect: true },
						{ text: "The Legend of Zelda: Tears of the Kingdom", isCorrect: false },
					],
				},
				{
					title: "Question 17",
					text: "Dans quel jeu il n'y a pas le personnage de Zelda ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 17,
					possibleAnswers: [
						{ text: "The Legend of Zelda: Link's Awakening", isCorrect: true },
						{ text: "The Legend of Zelda: The Minish Cap", isCorrect: false },
						{ text: "The Legend of Zelda: Oracle of Seasons", isCorrect: false },
						{ text: "The Legend of Zelda: Oracle of Ages", isCorrect: false },
						{ text: "Tous", isCorrect: false },
					],
				},
				{
					title: "Question 18",
					text: "Link est-il amoureux de Zelda ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 18,
					possibleAnswers: [
						{ text: "Vrai", isCorrect: false },
						{ text: "Faux", isCorrect: false },
						{ text: "On ne sait pas", isCorrect: true },
					],
				},
				{
					title: "Question 19",
					text: "Lequel n'est pas l'antagoniste d'un jeu Zelda ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 19,
					possibleAnswers: [
						{ text: "Ganondorf", isCorrect: false },
						{ text: "Kimado", isCorrect: false },
						{ text: "Avatar du Néant", isCorrect: false },
						{ text: "Giralui", isCorrect: true },
					],
				},
				{
					title: "Question 20",
					text: "Quelle console n'a pas eu de version collector Zelda ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 20,
					possibleAnswers: [
						{ text: "GameBoy Advance SP", isCorrect: false },
						{ text: "Wii U", isCorrect: false },
						{ text: "GameCube", isCorrect: true },
						{ text: "DS Lite", isCorrect: false },
					],
				},
				{
					title: "Question 21",
					text: "Quel collector contient une figurine de Ganondorf ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 21,
					possibleAnswers: [
						{ text: "The Legend of Zelda: Twilight Princess HD", isCorrect: false },
						{ text: "The Legend of Zelda: Twilight Princess", isCorrect: false },
						{ text: "The Legend of Zelda: The Wind Waker", isCorrect: false },
						{ text: "The Legend of Zelda: The Wind Waker HD", isCorrect: true },
					],
				},
				{
					title: "Question 22",
					text: "Quel jeu n'est pas ressorti plus tard (remake, remaster et portage) ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 22,
					possibleAnswers: [
						{ text: "The Legend of Zelda: A Link to the Past", isCorrect: false },
						{ text: "The Legend of Zelda: Four Swords Adventures", isCorrect: true },
						{ text: "The Legend of Zelda: Four Swords", isCorrect: false },
						{ text: "The Legend of Zelda", isCorrect: false },
					],
				},
				{
					title: "Question 23",
					text: "Quel est le jeu Zelda qui a introduit les fragments de cœur ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 23,
					possibleAnswers: [
						{ text: "The Legend of Zelda", isCorrect: false },
						{ text: "Zelda II: The Adventure of Link", isCorrect: false },
						{ text: "The Legend of Zelda: A Link to the Past", isCorrect: true },
						{ text: "The Legend of Zelda: Link's Awakening", isCorrect: false },
					],
				},
				{
					title: "Question 24",
					text: "Quel est le nom du bateau dans The Legend of Zelda: The Wind Waker ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 24,
					possibleAnswers: [
						{ text: "Le Lion Rouge", isCorrect: true },
						{ text: "Le Roi des Mers", isCorrect: false },
						{ text: "Le Bateau Fantôme", isCorrect: false },
						{ text: "Le Vaisseau des Ombres", isCorrect: false },
					],
				},
				{
					title: "Question 25",
					text: "Quel est le sous-titre du jeu The Legend of Zelda sur NES en version japonaise ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 25,
					possibleAnswers: [
						{ text: "Hyrule Fantasy", isCorrect: true },
						{ text: "The Adventures of Link", isCorrect: false },
						{ text: "Quest for the Triforce", isCorrect: false },
						{ text: "The Golden Power", isCorrect: false },
					],
				},
				{
					title: "Question 26",
					text: "Quel est le nom de l'arme principale de Link dans The Legend of Zelda: Skyward Sword ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 26,
					possibleAnswers: [
						{ text: "Lame Purificatrice", isCorrect: false },
						{ text: "Lame de la Déesse", isCorrect: false },
						{ text: "L'épée Divine", isCorrect: true },
						{ text: "L'épée de Légende", isCorrect: false },
					],
				},
				{
					title: "Question 27",
					text: "Dans The Legend of Zelda: Breath of the Wild, combien de sanctuaires faut-il compléter pour obtenir toutes les âmes ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 27,
					possibleAnswers: [
						{ text: "120", isCorrect: true },
						{ text: "80", isCorrect: false },
						{ text: "100", isCorrect: false },
						{ text: "150", isCorrect: false },
					],
				},
				{
					title: "Question 28",
					text: "Quel est le nom de la tribu habitant la montagne de la Mort dans The Legend of Zelda: Ocarina of Time ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 28,
					possibleAnswers: [
						{ text: "Les Gorons", isCorrect: true },
						{ text: "Les Zoras", isCorrect: false },
						{ text: "Les Gerudos", isCorrect: false },
						{ text: "Les Kokiris", isCorrect: false },
					],
				},
				{
					title: "Question 29",
					text: "Quel est le nom du dragon de feu dans The Legend of Zelda: Breath of the Wild ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 29,
					possibleAnswers: [
						{ text: "Rordrac", isCorrect: false },
						{ text: "Ordrac", isCorrect: true },
						{ text: "Nedrac", isCorrect: false },
						{ text: "Volvagia", isCorrect: false },
					],
				},
				{
					title: "Question 30",
					text: "Dans quel jeu Zelda peut-on retrouver Tetra ?",
					image: "/src/assets/zelda-placeholder.jpg",
					position: 30,
					possibleAnswers: [
						{ text: "The Legend of Zelda: The Wind Waker", isCorrect: true },
						{ text: "The Legend of Zelda: Majora's Mask", isCorrect: false },
						{ text: "The Legend of Zelda: Twilight Princess", isCorrect: false },
						{ text: "The Legend of Zelda: Link's Awakening", isCorrect: false },
					],
				}
			],
		};
	},
	mounted() {
	},
}

</script>

<style>
.db-title {
	text-align: center;
}

.database-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: var(--color-background-soft);
	border-radius: 5px;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	padding: 20px;
}

.database-buttons {
	display: flex;
}

.database-buttons button {
	margin: 10px;
	padding: 10px 20px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

.database-buttons button.empty {
	background-color: var(--vt-c-important);
	color: var(--vt-c-accent-text);
}

.database-buttons button.empty:hover {
	background-color: var(--vt-c-important-light);
}

.database-buttons button.load-default {
	background-color: var(--vt-c-tertiary);
	color: var(--vt-c-accent-text);
}

.database-buttons button.load-default:hover {
	background-color: var(--vt-c-tertiary-light);
}
</style>