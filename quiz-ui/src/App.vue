<script setup>
import { RouterLink, RouterView } from 'vue-router'
import LogoImage from '/src/assets/logo.png';
</script>

<template>
  <div class="app-container">
    <header class="menu-container">
      <div class="logo">
        <!-- Affichage du logo -->
        <img :src="LogoImage" alt="Quiz Logo" class="logo-image" />
      </div>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/Admin">Admin</RouterLink>
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
}

.menu-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  width: 200px; /* Ajustez cette valeur selon vos besoins */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.logo {
  margin-bottom: 2rem;
}

.logo-image {
  max-width: 150px; /* Augmenter la taille du logo */
  height: auto;
}

nav {
  width: 100%;
  font-size: 1rem;
  text-align: center;
}

nav a {
  display: block;
  padding: 0.5rem 0;
  text-decoration: none;
  color: var(--color-text);
}

nav a.router-link-exact-active {
  font-weight: bold;
}

.content {
  flex-grow: 1;
  padding: 2rem;
  margin-left: 50px; /* Espace entre le menu et le contenu */
  justify-content: center; /* Centrer horizontalement le contenu */
  align-items: center; /* Centrer verticalement le contenu */
}
</style>
