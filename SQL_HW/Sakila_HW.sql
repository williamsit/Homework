-- 1a. Display the first and last names of all actors from the table actor.

SELECT 
    first_name, last_name
FROM
    sakila.actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.

SELECT 
    UPPER(CONCAT(first_name, ' ', last_name)) AS 'Actor Name'
FROM
    sakila.actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?

SELECT 
    actor_id, CONCAT(first_name, ' ', last_name) AS 'Actor Name'
FROM
    sakila.actor
WHERE
    first_name = 'Joe';

-- 2b. Find all actors whose last name contain the letters GEN:

SELECT 
    actor_id, CONCAT(first_name, ' ', last_name) AS 'Actor Name'
FROM
    sakila.actor
WHERE
    last_name LIKE '%gen%';

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:

SELECT 
    actor_id, CONCAT(first_name, ' ', last_name) AS 'Actor Name'
FROM
    sakila.actor
WHERE
    last_name LIKE '%li%'
ORDER BY last_name , first_name;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
 
SELECT 
    country_id, country
FROM
    sakila.country
WHERE
    country IN ('Afghanistan' , 'Bangladesh', 'China');

-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).

alter table sakila.actor add column description blob after last_name;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.

alter table sakila.actor drop column description;

-- 4a. List the last names of actors, as well as how many actors have that last name.

SELECT 
    last_name, COUNT(last_name) AS last_name_count
FROM
    sakila.actor
GROUP BY last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors

SELECT 
    last_name, COUNT(last_name) AS last_name_count
FROM
    sakila.actor
GROUP BY last_name
HAVING last_name_count >= 2;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.

UPDATE sakila.actor 
SET 
    first_name = 'HARPO'
WHERE
    first_name = 'GROUCHO'
        AND last_name = 'WILLIAMS';

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.

UPDATE sakila.actor 
SET 
    first_name = 'GROUCHO'
WHERE
    first_name = 'HARPO'
        AND last_name = 'WILLIAMS';

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?

show create table address;
describe sakila.address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:

SELECT 
    CONCAT(s.first_name, ' ', s.last_name) AS 'Staff Name',
    a.address
FROM
    sakila.staff s
        INNER JOIN
    sakila.address a ON s.address_id = a.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.

SELECT 
    CONCAT(s.first_name, ' ', s.last_name) AS 'Staff Name',
    SUM(p.amount) AS 'Total Amount'
FROM
    sakila.staff s
        INNER JOIN
    sakila.payment p ON s.staff_id = p.staff_id
GROUP BY s.first_name , s.last_name;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.

SELECT 
    f.title, COUNT(a.actor_id) AS total_actors
FROM
    sakila.film f
        INNER JOIN
    sakila.film_actor a ON f.film_id = a.film_id
GROUP BY f.title;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?

SELECT 
    title,
    (SELECT 
            COUNT(*)
        FROM
            sakila.inventory
        WHERE
            film.film_id = inventory.film_id) AS 'Count of Films'
FROM
    sakila.film
WHERE
    title = 'HUNCHBACK IMPOSSIBLE';

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:

SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS 'Customer Name',
    SUM(p.amount) AS 'Total Amount'
FROM
    sakila.customer c
        JOIN
    payment p ON c.customer_id = p.customer_id
GROUP BY c.last_name
ORDER BY c.last_name ASC;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.

SELECT 
    title AS 'Film Title'
FROM
    sakila.film
WHERE
    title LIKE 'K%'
        OR title LIKE 'Q%'
        AND language_id = (SELECT 
            language_id
        FROM
            sakila.language
        WHERE
            name = 'ENGLISH');
 
-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.

SELECT 
    CONCAT(first_name, ' ', last_name) AS 'Actor Name'
FROM
    sakila.actor
WHERE
    actor_id IN (SELECT 
            actor_id
        FROM
            sakila.film_actor
        WHERE
            film_id IN (SELECT 
                    film_id
                FROM
                    film
                WHERE
                    title = 'ALONE TRIP'));
    
-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.

SELECT 
    CONCAT(first_name, ' ', last_name) AS 'Customer Name',
    email AS 'Email'
FROM
    sakila.customer cu
        JOIN
    address a ON (cu.address_id = a.address_id)
        JOIN
    city cit ON (a.city_id = cit.city_id)
        JOIN
    country cnty ON (cit.country_id = cnty.country_id)
WHERE
    cnty.country = 'Canada';

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.

SELECT 
    title AS 'Film Title', description AS 'Film Description'
FROM
    sakila.film
WHERE
    film_id IN (SELECT 
            film_id
        FROM
            sakila.film_category
        WHERE
            category_id IN (SELECT 
                    category_id
                FROM
                    sakila.category
                WHERE
                    name = 'FAMILY'));
        
-- 7e. Display the most frequently rented movies in descending order.

SELECT 
    title AS 'Film Title',
    COUNT(f.film_id) AS 'Count of Rented Movies'
FROM
    sakila.film f
        JOIN
    sakila.inventory i ON (f.film_id = i.film_id)
        JOIN
    sakila.rental r ON (i.inventory_id = r.inventory_id)
GROUP BY title
ORDER BY COUNT(f.film_id) DESC;

-- 7f. Write a query to display how much business, in dollars, each store brought in.

SELECT 
    s.store_id AS 'Store ID', SUM(p.amount) AS 'Revenue'
FROM
    sakila.payment p
        JOIN
    sakila.rental r ON (p.rental_id = r.rental_id)
        JOIN
    sakila.inventory i ON (i.inventory_id = r.inventory_id)
        JOIN
    sakila.store s ON (s.store_id = i.store_id)
GROUP BY s.store_id;

-- 7g. Write a query to display for each store its store ID, city, and country.

SELECT 
    s.store_id AS 'Store ID',
    cty.city AS 'City',
    cnty.country AS 'Country'
FROM
    sakila.store s
        JOIN
    sakila.address a ON (s.address_id = a.address_id)
        JOIN
    sakila.city cty ON (a.city_id = cty.city_id)
        JOIN
    sakila.country cnty ON (cty.country_id = cnty.country_id);

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)

SELECT 
    c.name AS 'Genre', SUM(p.amount) AS 'Gross Revenue'
FROM
    category c
        JOIN
    film_category fc ON (c.category_id = fc.category_id)
        JOIN
    inventory i ON (fc.film_id = i.film_id)
        JOIN
    rental r ON (i.inventory_id = r.inventory_id)
        JOIN
    payment p ON (r.rental_id = p.rental_id)
GROUP BY c.name
ORDER BY SUM(p.amount) DESC
LIMIT 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.

CREATE VIEW genre_revenue AS
    SELECT 
        c.name AS 'Genre', SUM(p.amount) AS 'Gross Revenue'
    FROM
        category c
            JOIN
        film_category fc ON (c.category_id = fc.category_id)
            JOIN
        inventory i ON (fc.film_id = i.film_id)
            JOIN
        rental r ON (i.inventory_id = r.inventory_id)
            JOIN
        payment p ON (r.rental_id = p.rental_id)
    GROUP BY c.name
    ORDER BY SUM(p.amount) DESC
    LIMIT 5;

-- 8b. How would you display the view that you created in 8a?

SELECT 
    *
FROM
    genre_revenue;

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.

drop view genre_revenue;
