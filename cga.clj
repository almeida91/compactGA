(defn generate-candidate
  ([prob-vector] (generate-candidate prob-vector []))
  ([prob-vector candidate]
   (if (empty? prob-vector)
     (clojure.string/join "" candidate)
     (let [random (new java.util.Random)]
       (recur (rest prob-vector) (into candidate (if (< (. random nextDouble) (first prob-vector)) "1" "0")))))))

(defn generate-vector [size] (vec (repeat size 0.5)))

(defn compete
  [a b]
  (if (> (:fitness a) (:fitness b))
    [a b]
    [b a]))

(defn update-vector
  [prob-vector winner loser population-size]
  (loop [final-vector [] remaining-winner winner remaining-loser loser prob prob-vector]
    (if (= (count prob) 0)
      final-vector
      (if (and (not (= (first remaining-winner) (first remaining-loser))) (= (first winner) "1"))
        (recur (into final-vector [(+ (first prob) (/ 1.0 population-size))]) (rest remaining-winner) (rest remaining-loser) (rest prob))
        (recur (into final-vector [(- (first prob) (/ 1.0 population-size))]) (rest remaining-winner) (rest remaining-loser) (rest prob))
        ))))

(defn calculate-fitness
  [fitness-function solution]
  {:value solution :fitness (fitness-function solution)})

(defn run
  [generations size population-size fitness-function]
  (loop [best nil generation 0 prob-vector (generate-vector size)]
    (if (>= generation generations)
      best
      (do
        (println "Generation #" generation)
        (def s1 (generate-candidate prob-vector))
        (def s2 (generate-candidate prob-vector))

        (let [[winner loser] (compete (calculate-fitness fitness-function s1) (calculate-fitness fitness-function s2))]
          (recur (if (nil? best) winner (if (> (:fitness winner) (:fitness best)) winner best))
                 (inc generation)
                 (update-vector prob-vector winner loser population-size)))))))

(println (run 1000 10 10 #(Integer/parseInt % 2)))
