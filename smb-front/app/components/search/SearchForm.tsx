import React from "react";
import './Search.css'
import {InputMask} from "@react-input/mask";

interface SearchFormProp {
    searchQuery: string;
    setSearchQuery: (value: string | ((prevState: string) => string)) => void;
    handleSearch: (e: React.FormEvent) => void;
}

const SearchForm: React.FC<SearchFormProp> = ({ searchQuery, setSearchQuery, handleSearch }) => {
    return (
        <form className="search-form" onSubmit={handleSearch}>
            <div className="search-input-wrapper">
                <svg className="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3C5.91 3 3 5.91 3 9.5C3 13.09 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5C5 7.01 7.01 5 9.5 5C11.99 5 14 7.01 14 9.5C14 11.99 11.99 14 9.5 14Z" fill="#94a3b8"/>
                </svg>

                <InputMask
                    className="search-input"
                    mask="__ __ ______ __" replacement={{ _: /\d/ }}
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />

                {searchQuery && (
                    <button
                        type="button"
                        className="clear-search"
                        onClick={() => setSearchQuery('')}
                    >
                        ×
                    </button>
                )}
            </div>
            <button type="submit" className="search-button">
                Анализировать
            </button>
        </form>
    )
}

export default SearchForm;