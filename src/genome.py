"""A circular genome for simulating transposable elements."""

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)


class Genome(ABC):
    """Representation of a circular enome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet

    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet


class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = [('-', 0) for _ in range(n)] # genome with no TEs 
        # created.
        self.active_TEs = {} # dictionary for active TEs 
        # where the key is a TE ID and the value is a tuple with the 
        # start pos of the TE and the length of the TE.  
        self.inactive_TEs = {} # dictionary for inactive tes.
        self.number_of_TEs = 0 # counter

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """

        # Get ID of TE. 
        self.number_of_TEs += 1
        id = self.number_of_TEs

        # create TE. 
        te = []
        for i in range(length):
            te.append(('A', id))
        
        # test whether active TE in pos of genome, where the new TE is
        # inserted.
        if self.genome[pos][0] == 'A':
            # determine TE found at pos.
            te_to_be_disabled = self.genome[pos][1] 
            # disable TE found at pos.
            self.disable_te(te_to_be_disabled)

        # insert TE into genome. 
        self.genome[pos:pos] = te

        # Update dictionary for active TE and for inactive TE.
        self.active_TEs[id] = (pos, length)

        # update start pos of active TEs found after the newly inserted
        # TE. Inactive TEs not of interest. 
        for te in self.active_TEs: # te is the key in the dict and an id. 
            # if the start pos of the te is found after pos, add length
            # to the start pos. 
            if self.active_TEs[te][0] > pos:
                self.active_TEs[te] = (self.active_TEs[te][0]+length, self.active_TEs[te][1])
        return id

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """         
        # obtain information regarding the TE to be copied.
        id_original = te
        start_position_original = self.active_TEs[te][0] 
        length = self.active_TEs[te][1] # length_original ofc the 
        # same as length_new.
        # determine position that the copy is to be inserted at.
        start_position_new = (start_position_original + offset)%len(self.genome)
        # insert copy. 
        id_new = self.insert_te(start_position_new, length)
        return id_new

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """ 
        # Obtain attributes for TE.
        id = te
        start_pos_of_te = self.active_TEs[id][0]
        length_of_te = self.active_TEs[id][1]
        
        # Change 'A' in self.genome to x where the TE is found.
        for n in range(start_pos_of_te, start_pos_of_te+length_of_te):
            self.genome[n] = ('x', id) # n is a tuple: (nucleotide, id)

        if te in self.active_TEs:
            self.inactive_TEs[te] = self.active_TEs.pop(te)


    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.active_TEs)
 
    def __len__(self) -> int:
        """Current length of the genome."""
        length = len(self.genome)
        return length

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        representation = ''
        for n in self.genome:
            representation += n[0]
        return representation


# The genome is circular.
class Nucleotide(object):
    def __init__(self, symbol='-', id=None):
        self.symbol = symbol
        self.id = id

    def __repr__(self): # machine readable textual representation.
        return f"Nucleotide('{self.symbol}', {self.id})"
    
    def __str__(self): # human readable textual representation.
        return self.symbol


class TE(object):
    def __init__(self, id, pos, seq, length, status='active'):
        self.id = id
        self.pos = pos
        self.seq = seq # list of nucleotides. 
        self.length = length
        self.status = status # 'active' or 'inactive'

    def __repr__(self):
        return f"TE({self.id}, {self.pos}, {self.seq}, {self.length}, '{self.status}')"


class DoublyLink(object):
    def __init__(self, element, previous, next):
        self.element = element
        self.previous = previous
        self.next = next
    
    def repr(self):
        return 'DoublyLink({}, {})'.format(
            repr(self.element), 
            repr(self.next)
        )
 
def insert_after(link, element):
    new_link = DoublyLink(element, link, link.next)
    new_link.previous.next = new_link
    new_link.next.previous = new_link

class DoublyLinkedListSequence(object):
    def __init__(self, seq = ()):
        """Create empty circular DoublyLinkedListSequence"""
        self.head = DoublyLink(None, None, None)
        self.head.prev = self.head
        self.head.next = self.head

        for element in seq:
            insert_after(self.head.prev, element)

    def __str__(self):
        """
        Get string representation.
        """
        lst = []
        link = self.head.next
        while link is not self.head:
            lst.append(str(link.element))
            link = link.next
        return f"{''.join(lst)}"
    __repr__ = __str__

    def __len__(self):
        len = 0
        link = self.head.next
        while link is not self.head:
            len += 1
            link = link.next
        return len

    def get_link_at_index(self, index):
        if index < 0:
            raise IndexError('Negative Index')
        link = self.head.next
        while link is not self.head:
            if index == 0:
                return link
            link = link.next
            index -= 1
        raise IndexError('Index out of range')
    
    def get_element_at_index(self, index):
        return self.get_link_at_index(index).element

    def set_at_index(self, index, element):
        self.get_link_at_index(index).element = element

    def insert_list_after_link(self, link, begin, end): # p. 423
        end.next = link.next
        end.next.previous = end
        begin.previous = link
        begin.previous.next = begin


class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        # make empty DoublyLinkedListSequence.
        nucleotides = [Nucleotide() for _ in range(n)]
        self.genome = DoublyLinkedListSequence(nucleotides)
        self.tes = [] 

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        # create new TE-object
        id = len(self.tes)+1
        seq = DoublyLinkedListSequence()
        for _ in range(length): 
            insert_after(seq.head, Nucleotide('A', id)) 
        te = TE(id, pos, seq, length) # te.status='active' by default. 
        
        # test whether an active TE is already found at pos.
        nucleotide = self.genome.get_element_at_index(pos)
        if nucleotide.symbol == 'A':
            # change 'A' to x in self.genome
            id_old = nucleotide.id
            te_old = self.tes[id_old-1]
            for index in range(te_old.pos, te_old.pos+te_old.length):
                self.genome.set_at_index(index, Nucleotide('x', id_old))
            # disable te in tes
            te_old.status = 'inactive'

        # get link that the TE is to be inserted after. 
        if pos != 0:
            link = self.genome.get_link_at_index(pos-1) 
        else: # if pos == 0
            link = self.genome.head
         # insert newly made TE in self.genome
        self.genome.insert_list_after_link(link, te.seq.head.next, te.seq.head.previous)

        # add new TE to tes list.
        self.tes.append(te)
        
        # update pos of TEs found after the newly inserted TE.
        for te in self.tes:
            if te.pos > pos:
                te.pos += length
        return id

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        id = te
        te = self.tes[id-1]
        if te.status == 'active': # Only an active TE can be copied. 
            start_pos_original = te.pos
            length_genome = len(self.genome)
            start_pos_copy = (offset + start_pos_original)%length_genome 
            # Nødvendigt med %length_genome til sidst, in case addition
            # med start_pos original gør, så start_pos_copy ikke er 
            # indenfor index range af genomet. 
            # Hvis offset+start_pos_original er negativ, vil python
            # alligevel returnere et positivt tal ved modulo. Hvis 
            # hvis offset+start_pos_original fx er -2, vil python
            # returnere indexet length_genome-2, da
            # index -2 = index lenght_genome-2. Dvs. python omdanner
            # blot det negative index til et positivt index.
            id_new = self.insert_te(start_pos_copy, te.length)
            return id_new
        return None

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        # id is equal to the position of the TE in the te-list + 1. 
        id = te
        te = self.tes[id-1]
        # change nucleotides in genome from 'A' to x.
        for n in range(te.pos, te.pos+te.length):
            self.genome.get_element_at_index(n).symbol = 'x' 
        te.status = 'inactive'

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        active = []
        for te in self.tes:
            if te.status == 'active':
                active.append(te.id)
        return active

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.genome)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        return repr(self.genome)


print('linked list genome')
genome = LinkedListGenome(20) 
print(genome)
print(genome.active_tes())

genome.insert_te(5, 10) # 
print(genome)
print(genome.active_tes()) # [1]

genome.insert_te(10, 10)
print(genome)
print(genome.active_tes()) 

genome.copy_te(2, 20)
print(genome)
print(genome.active_tes())

genome.copy_te(2, -15)
print(genome)
print(genome.active_tes())

genome.insert_te(50, 10)
print(genome)
print(genome.active_tes())

genome.disable_te(3)
print(genome)
print(genome.active_tes())

# test if TE can be copied to a position larger than the genome.
# test whether start pos of TEs after an newly inserted TE are updated.
genome2 = LinkedListGenome(20)
genome2.insert_te(10, 10)
print(genome2)
print(genome2.tes[0].pos)

genome2.copy_te(1, 22)
print(genome2) 
print(genome2.tes[0].pos)
print(genome2.tes[1].pos)

genome2.insert_te(0, 10)
print(genome2)
print(genome2.tes[0].pos)
print(genome2.tes[1].pos) 

print('list genome')
genome = ListGenome(20) 
print(genome)
print(genome.active_tes())

genome.insert_te(5, 10) # 
print(genome)
print(genome.active_tes()) # [1]

genome.insert_te(10, 10)
print(genome)
print(genome.active_tes()) 

genome.copy_te(2, 20)
print(genome)
print(genome.active_tes())

genome.copy_te(2, -15)
print(genome)
print(genome.active_tes())

genome.insert_te(50, 10)
print(genome)
print(genome.active_tes())

genome.disable_te(3)
print(genome)
print(genome.active_tes())

# test if TE can be copied to a position larger than the genome.
# test whether start pos of TEs after an newly inserted TE are updated.
genome2 = ListGenome(20)
genome2.insert_te(10, 10)
print(genome2)
print(genome2.active_tes())

genome2.copy_te(1, 22)
print(genome2) 
print(genome2.active_tes())

genome2.insert_te(0, 10)
print(genome2)
print(genome2.active_tes())
