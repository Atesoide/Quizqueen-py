create database quizqueen;

use quizqueen;
CREATE TABLE `cuestionario_prueba` (
  `id` int(11) NOT NULL,
  `pregunta` varchar(100) NOT NULL,
  `respuesta_1` varchar(100) NOT NULL,
  `respuesta_2` varchar(100) NOT NULL,
  `respuesta_3` varchar(100) NOT NULL,
  `respuesta_4` varchar(100) NOT NULL,
  `respuesta_correcta` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
CREATE TABLE  `usuarios` (
	`id` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre` varchar(50) NOT NULL,
    `correo` varchar(50) NOT NULL unique,
    `contraseña` varchar(100) NOT NULL,
    `rango`int(5),
    `puntuacion` int(20)
);

ALTER TABLE usuarios
ADD CONSTRAINT chk_email_format CHECK (
    correo REGEXP '^[a-zA-Z0-9][a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~]*?[a-zA-Z0-9._-]?@[a-zA-Z0-9][a-zA-Z0-9._-]*?[a-zA-Z0-9]?\\.[a-zA-Z]{2,63}$'
);

SELECT * FROM usuarios;
--
-- Dumping data for table `cuestionario_prueba`
--
INSERT INTO `usuarios` (nombre, correo, contraseña, rango, puntuacion) VALUES
('Atesoide', 'sample@gmail.com', '1234', '1', '100');
INSERT INTO `cuestionario_prueba` (`id`, `pregunta`, `respuesta_1`, `respuesta_2`, `respuesta_3`, `respuesta_4`, `respuesta_correcta`) VALUES
(1, '¿Cuál color se obtiene al mezclar rojo y azul? ', 'Verde ', 'Amarillo', 'Morado', 'Fucsia', 3),
(2, '¿Cuál es la tercer vocal del abecedario? ', 'I', 'U', 'O', 'E', 1),
(3, '¿Cuál de los siguientes personajes pertenece a la franquicia de Five Nights at Freddy\'s? ', 'Poppy Playtime', 'Vulpix', 'Ralph el Demoledor', 'Freddy Fazbear ', 4),
(4, '¿Cuál de los siguientes es un sabor de nieve? ', 'Vainilla ', 'Bolsa de papel', 'Plástico PET', 'Monopoly Bid ', 1),
(5, '¿Cuál de los siguientes es un Pokémon tipo normal?', 'Alolan Vulpix ', 'Eevee ', 'Ghastly', 'Raichu ', 2),
(6, '¿A qué temperatura hierve el agua a nivel del mar? ', '0° Kelvin ', '32° Farenheit ', '12° Celsius ', '100° Celsius', 4),
(7, '¿Cuáles elementos se encuentran principalmente en los seres vivos? ', 'Carbono, Hidrógeno, Oxígeno, Nitrógeno', 'Carbono, Calcio, Helio, Nitrógeno', 'Carbono, Hidrógeno, Xenón, Fósforo', 'Carbono, Hidrógeno, Calcio, Nitrógeno ', 1),
(8, '¿Qué significa PH? ', 'Puro Hidrógeno ', 'Potencial de Helio', 'Potencial de Hidrógeno ', 'Puros Hidroxilos ', 3),
(9, '¿Cuáles números tiene la escala del PH? ', 'Del 0 al 10', 'Del 0 al 14', 'Del 7 al 10', 'Del 7 al 14', 2),
(10, '¿Cuál de los siguientes personajes NO pertenece a la saga de FullMetal Alchemist Brotherhood? ', 'Edward Elric', 'Roy Mustang ', 'John Wick ', 'Mei Chang ', 3),
(11, '¿Cuál de las siguientes serpientes pertenece a la familia Boide?', 'Boa Constrictor Imperator', 'Python Regius', 'Crotalus Viridis', 'Pantherophis guttatus', 1),
(12, '¿Cuál de los siguientes colores NO se considera como color primario?', 'Rojo', 'Amarillo', 'Azul', 'Verde', 4),
(13, '¿Cuál de los siguentes se considera como el único marsupial del continente americano? ', 'El jaguar', 'El oso pardo', 'El tlacuache ', 'El capibara', 3),
(14, '¿Cuál de los siguientes animales se considera como invertebrado?', 'Araña', 'Leopardo', 'Pez', 'Delfín ', 1),
(15, 'What\'s 9 + 10?', '11', '19', '14', '21', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cuestionario_prueba`
--
ALTER TABLE `cuestionario_prueba`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cuestionario_prueba`
--
ALTER TABLE `cuestionario_prueba`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;
