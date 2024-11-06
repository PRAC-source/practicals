pragma solidity ^0.8.0;  // Corrected Solidity version

contract SimpleBank {
    struct client_account{ 
        int client_id;  
        address client_address;
        uint client_balance_in_ether;   
    } 

    client_account[] clients;

    int clientCounter;
    address payable manager; 


modifier onlyManager() {//modifier can check wheather code is executed according to condition for manager side 
         require(msg.sender == manager, "Only manager can call this!"); // here sender is manager in this case
// for deposit sender is == manager and for withdrawal sender== client when the function should be executed.
        _; 

    } 


modifier onlyClients() { //modifier can check wheather code is executed according to condition for client side 
        bool isclient = false;
         
         for(uint i=0;i<clients.length;i++){
            if(clients[i].client_address == msg.sender){
                isclient = true;  // client address matched with existing client address in bank database isclient value updated true.
                break;  
            } 

        }
       require(isclient, "Only clients can call this!"); 
       _;
    }


   constructor() { 
      clientCounter = 0;

    }

receive() external payable{ }


function setManager(address managerAddress) public returns(string memory){ //setManager method will be used to set the manager address to variables
        manager = payable(managerAddress);// managerAddress is consumed as a parameter and cast as payable to provide sending ether.
       return "";
   }


  function joinAsClient() public payable returns(string memory){
     clients.push(client_account(clientCounter++, msg.sender, 
      address(msg.sender).balance));
return "";

    }

function deposit() public payable onlyClients{
        // We want this method to be callable only by clients who’ve joined the contract
         payable(address(this)).transfer(msg.value);
       }
  function withdraw(uint amount) public payable onlyClients{ 

           payable(msg.sender).transfer(amount * 1 ether); 
//The address of the sender( ie contract ) is held in the msg.sender variable.
    }

  function getContractBalance() public view returns(uint){
    return address(this).balance;

}
}
