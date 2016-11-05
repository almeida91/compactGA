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
  (map (fn [prob win lost]
         (if (and (not= win lost) (= win "1"))
           (+ prob (/ 1.0 population-size))
           (- prob (/ 1.0 population-size))
           )) prob-vector winner loser))

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
