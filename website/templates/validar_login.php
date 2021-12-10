<?php
   session_start();
    if ($_POST["palavra"] == $_SESSION["palavra"]){
        echo "<h1>Voce Acertou</h1>";
        echo "<form action='login' name='form' method='post'>
            <input type='submit' value='Retornar' />
            </form>";
    }else{
        echo "<h1>Voce nao acertou!</h1>";
        echo "<form action='index_login.php' name='form' method='post'>
            <input type='submit' value='Retornar' />
            </form>";
    }
?>