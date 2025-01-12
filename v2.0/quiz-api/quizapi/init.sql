--Dane logowania:
--Bartek, bartek@wp.pl, haslo1
--Filip, filip@wp.pl, filip123
--Kinga, kinga@wp.pl, haselko

docker exec -it db psql -U postgres
\c app;

INSERT INTO players (username, email, password, balance) VALUES ('Bartek', 'bartek@wp.pl', '$2b$12$jZPX5HJm.TSBcJ3j3z956u.LSdZOwD.gOleO.wkqDyGOQPlJ6s8Ju', 100),('Filip', 'filip@wp.pl', '$2b$12$7yK29ce60byY5KV8EJ36heMuVqja55BgP3P6euZUj9MCCtx7vAlTa', 0),('Kinga', 'kinga@wp.pl', '$2b$12$KUl5qdIKqrAwHKedSmqVs.AZ86vZsRX6pvVsmWLcDvsPEK5500auO', 1000);

INSERT INTO quizzes (title, player_id, description, shared, reward) VALUES ('Matematyka dla początkujących', (SELECT id FROM players WHERE username = 'Bartek'), 'Podstawowe pytania matematyczne', TRUE, 'Medal za Matematykę'),('Historia Polski', (SELECT id FROM players WHERE username = 'Filip'), 'Test z historii Polski', FALSE, 'Złoty Puchar Historii'),('Quiz o zwierzętach', (SELECT id FROM players WHERE username = 'Kinga'), 'Ciekawostki o zwierzętach', TRUE, 'Srebrna Odznaka Przyrodnika');

INSERT INTO questions (question_text, option_one, option_two, option_three, option_four, correct_option, quiz_id) VALUES ('Ile wynosi 2 + 2?', '3', '4', '5', '6', '4', (SELECT id FROM quizzes WHERE title = 'Matematyka dla początkujących')), ('Pierwiastek kwadratowy z 9 to?', '2', '3', '4', '5', '3', (SELECT id FROM quizzes WHERE title = 'Matematyka dla początkujących')), ('Jaki jest wynik 5 * 6?', '25', '30', '35', '40', '30', (SELECT id FROM quizzes WHERE title = 'Matematyka dla początkujących')), ('W którym roku Polska odzyskała niepodległość?', '1918', '1939', '1863', '1795', '1918', (SELECT id FROM quizzes WHERE title = 'Historia Polski')), ('Bitwa pod Grunwaldem miała miejsce w roku?', '1320', '1410', '1683', '1772', '1410', (SELECT id FROM quizzes WHERE title = 'Historia Polski')), ('Kto był pierwszym królem Polski?', 'Mieszko I', 'Kazimierz Wielki', 'Bolesław Chrobry', 'Władysław Jagiełło', 'Bolesław Chrobry', (SELECT id FROM quizzes WHERE title = 'Historia Polski')),('Jakie zwierzę jest największym ssakiem na świecie?', 'Słoń', 'Wieloryb', 'Żyrafa', 'Hipopotam', 'Wieloryb', (SELECT id FROM quizzes WHERE title = 'Quiz o zwierzętach')),('Jakie zwierzę potrafi latać?', 'Pingwin', 'Nietoperz', 'Foka', 'Delfin', 'Nietoperz', (SELECT id FROM quizzes WHERE title = 'Quiz o zwierzętach')),('Które zwierzę najszybciej biega?', 'Gepard', 'Lew', 'Kangur', 'Wilk', 'Gepard', (SELECT id FROM quizzes WHERE title = 'Quiz o zwierzętach'));

INSERT INTO history (player_id, quiz_id, total_questions, correct_answers, effectiveness, timestamp) VALUES ((SELECT id FROM players WHERE username = 'Bartek'), (SELECT id FROM quizzes WHERE title = 'Matematyka dla początkujących'), 10, 8, 80.0, '2025-01-07T17:51:52.630Z'), ((SELECT id FROM players WHERE username = 'Filip'), (SELECT id FROM quizzes WHERE title = 'Historia Polski'), 12, 9, 75.0, '2025-01-07T18:15:32.125Z'), ((SELECT id FROM players WHERE username = 'Kinga'), (SELECT id FROM quizzes WHERE title = 'Quiz o zwierzętach'), 15, 14, 93.3, '2025-01-07T19:30:45.555Z'), ((SELECT id FROM players WHERE username = 'Bartek'), (SELECT id FROM quizzes WHERE title = 'Historia Polski'), 12, 10, 83.3, '2025-01-07T20:00:10.777Z'), ((SELECT id FROM players WHERE username = 'Filip'), (SELECT id FROM quizzes WHERE title = 'Quiz o zwierzętach'), 15, 12, 80.0, '2025-01-07T21:45:22.999Z'), ((SELECT id FROM players WHERE username = 'Kinga'), (SELECT id FROM quizzes WHERE title = 'Matematyka dla początkujących'), 10, 9, 90.0, '2025-01-07T22:10:05.333Z');

INSERT INTO tournaments (name, description, quizzes_id, participants) VALUES('Turniej Matematyczny', 'Turniej dla fanów matematyki', ARRAY[(SELECT id FROM quizzes WHERE title = 'Matematyka dla początkujących')], ARRAY[(SELECT id FROM players WHERE username = 'Bartek')]), ('Turniej Historyczny', 'Kto zna historię najlepiej?', ARRAY[(SELECT id FROM quizzes WHERE title = 'Historia Polski')], ARRAY[(SELECT id FROM players WHERE username = 'Filip')]), ('Turniej Przyrodniczy', 'Zmagania o tytuł eksperta przyrody', ARRAY[(SELECT id FROM quizzes WHERE title = 'Quiz o zwierzętach')], ARRAY[(SELECT id FROM players WHERE username = 'Kinga')]);

INSERT INTO rewards (quiz_id, player_id, reward, value) VALUES ((SELECT id FROM quizzes WHERE title = 'Matematyka dla początkujących'), (SELECT id FROM players WHERE username = 'Bartek'),(SELECT reward FROM quizzes WHERE title = 'Matematyka dla początkujących'),30), ((SELECT id FROM quizzes WHERE title = 'Historia Polski'), (SELECT id FROM players WHERE username = 'Filip'), (SELECT reward FROM quizzes WHERE title = 'Historia Polski'),30), ((SELECT id FROM quizzes WHERE title = 'Quiz o zwierzętach'), (SELECT id FROM players WHERE username = 'Kinga'), (SELECT reward FROM quizzes WHERE title = 'Quiz o zwierzętach'),30);