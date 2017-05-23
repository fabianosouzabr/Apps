<html>
    <ul>
        % for item in results:
            <li><a href='http://localhost:4567/item/{{item}}'>{{item}}</a></li>
        % end
    </ul>
</html>