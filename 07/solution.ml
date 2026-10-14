(* Advent of Code 2024, jour 7 : opérateurs pour atteindre une cible.

   Recherche récursive : à chaque nombre, on essaie chacun des opérateurs,
   donnés sous forme d'une liste de fonctions ; List.exists s'arrête au
   premier succès. Élagage : une branche est coupée dès que la valeur partielle
   dépasse la cible (somme, produit et concaténation ne font jamais décroître
   une valeur sur des entiers positifs), et la concaténation n'est proposée que
   si 10 * acc <= cible.
   Partie 1 : sans concaténation.
   L'accumulateur part du premier nombre : partir de 0 permettrait le choix
   « 0 * t », qui revient à ignorer le premier nombre (ex. cible 5 avec
   [3; 5] serait acceptée).

   Compilation :
     ocamlfind ocamlopt -package str -linkpkg solution.ml -o solution *)

let concat a b = int_of_string (string_of_int a ^ string_of_int b)

let rec search ops tgt acc = function
  | [] -> acc = tgt
  | _ when acc > tgt -> false
  | t :: q -> List.exists (fun f -> search ops tgt (f acc t) q) (ops acc tgt)

(* Opérateurs autorisés depuis la valeur partielle acc. *)
let ops1 _ _ = [ ( + ); ( * ) ]

let ops2 acc tgt =
  ( + ) :: ( * ) :: (if 10 * acc <= tgt then [ concat ] else [])

let read_equations filename =
  let ic = open_in filename in
  let rec loop acc =
    match input_line ic with
    | line when String.trim line = "" -> loop acc
    | line -> (
        match Str.split (Str.regexp ": ") line with
        | [ tgt; numbers ] ->
            let numbers =
              List.map int_of_string (Str.split (Str.regexp " +") numbers)
            in
            loop ((int_of_string tgt, numbers) :: acc)
        | _ -> failwith "ligne mal formée")
    | exception End_of_file ->
        close_in ic;
        List.rev acc
  in
  loop []

let total ops equations =
  List.fold_left ( + ) 0
    (List.map fst
       (List.filter
          (fun (tgt, numbers) ->
            match numbers with
            | [] -> false
            | t :: q -> search ops tgt t q)
          equations))

let () =
  let equations = read_equations "input.txt" in
  Printf.printf "Partie 1 : %d\n" (total ops1 equations);
  Printf.printf "Partie 2 : %d\n" (total ops2 equations)
