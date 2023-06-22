// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

contract SimpleStorage {
    uint256 favoriteNumber;

    // People public Person = People ({
    //     favoriteNumber: 7,
    //     name: "Crome"
    // });

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    mapping(string => uint256) public nameToFavoriteNumber;

    People[] public people;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
