<template>
  <div class="about-page">
    <div class="content">
      <h1 class="title">About This Website</h1>
      <p class="description">
        Welcome to our movie website! Here, you can explore a variety of features to enhance your movie-watching experience:
      </p>
      <ul>
        <li>On the homepage, we provide a list of the top 7 rated movies from each category, helping you discover the best films easily.</li>
        <li>You can search for movies by category, making it easy to find films that match your interests.</li>
      </ul>
      <p class="description">
        Our goal is to provide an easy-to-navigate platform for movie enthusiasts to find and explore their favorite films based on categories and ratings.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  
};
</script>

<style scoped>
.about-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.content {
  text-align: center;
  max-width: 800px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #333;
}

.description {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 15px;
}

ul {
  text-align: left;
  margin: 0 auto;
  display: inline-block;
  font-size: 1.1rem;
  color: #555;
}

li {
  margin-bottom: 10px;
}
</style>
